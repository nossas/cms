from django.conf import settings
from django.db import models

import boto3
import dns.resolver
from botocore.exceptions import ClientError


class HostedZone(models.Model):
    id = models.CharField(max_length=50, primary_key=True, auto_created=False)
    name = models.CharField(max_length=100)
    healtcheck = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def related_instances(self):
        rs1 = self.recordset_set.filter(
            record_type=RecordType.A, name=self.name
        ).first()
        rs2 = self.recordset_set.filter(
            record_type=RecordType.A, name="\\052." + self.name
        ).first()

        if (
            rs1
            and rs2
            and len(rs1.resource) > 0
            and len(rs2.resource) > 0
            and rs1.resource[0] == rs2.resource[0]
        ):
            return VPS.objects.filter(static_ip=rs1.resource[0])

        # if self.name == 'meurecife.org.br.':
        #     import ipdb;ipdb.set_trace()

        # lista = list(
        #     map(
        #         lambda x: x.vps, list(filter(lambda x: x.vps, self.recordset_set.all()))
        #     )
        # )

        return VPS.objects.none()

    def check_ns(self):
        record_set = self.recordset_set.filter(record_type="NS").first()

        try:
            for rdata in dns.resolver.query(self.name[:-1], "NS"):
                if str(rdata) in record_set.resource:
                    return True
        except Exception:
            return False

        return False

    def delete_on_route53(self):
        client = boto3.client(
            "route53",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            # aws_region=settings.AWS_REGION
        )

        response = client.delete_hosted_zone(Id=self.id)

        return response["ChangeInfo"]["Status"]


class RecordType(models.TextChoices):
    SOA = "SOA"
    A = "A"
    TXT = "TXT"
    NS = "NS"
    CNAME = "CNAME"
    MX = "MX"
    NAPTR = "NAPTR"
    PTR = "PTR"
    SRV = "SRV"
    SPF = "SPF"
    AAAA = "AAAA"
    CAA = "CAA"
    DS = "DS"


class RecordSet(models.Model):
    hosted_zone = models.ForeignKey(HostedZone, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    record_type = models.CharField(max_length=5, choices=RecordType.choices)
    resource = models.JSONField(blank=True, null=True)  # [""]

    def __str__(self):
        return self.name

    @property
    def vps(self):
        if self.record_type == RecordType.A and len(self.resource) > 0:
            vps = VPS.objects.filter(static_ip=self.resource[0]).first()
            if vps:
                return vps.name

        return None

    def delete_on_route53(self):

        if self.record_type != RecordType.NS and self.record_type != RecordType.SOA:
            client = boto3.client(
                "route53",
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                # aws_region=settings.AWS_REGION
            )

            try:
                response = client.change_resource_record_sets(
                    HostedZoneId=self.hosted_zone.id,
                    ChangeBatch={
                        "Changes": [
                            {
                                "Action": "DELETE",
                                "ResourceRecordSet": {
                                    "Name": self.name,
                                    "Type": self.record_type,
                                    "TTL": 300,
                                    "ResourceRecords": list(
                                        map(lambda x: dict(Value=x), self.resource)
                                    ),
                                },
                            }
                        ]
                    },
                )

                return response["ChangeInfo"]["Status"]
            except ClientError as err:
                print(err)


class VPS(models.Model):
    name = models.CharField(max_length=40)
    static_ip = models.GenericIPAddressField(unique=True)

    class Meta:
        verbose_name = "Instância"
        verbose_name_plural = "Instâncias"

    def __str__(self):
        return self.name
