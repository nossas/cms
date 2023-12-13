from django.conf import settings


class Manager:
    def __init__(self, name=None, fields=None):
        import boto3

        self.client = boto3.client(
            "route53",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            # aws_region=settings.AWS_REGION
        )

    def list_hosted_zones(self):
        response = self.client.list_hosted_zones()
        hosted_zones = response.get("HostedZones", [])

        return list(
            map(
                lambda x: HostedZone(id=x.get("Id", ""), name=x.get("Name", "")),
                hosted_zones,
            )
        )

    def get_hosted_zone(self, id):
        return self.client.get_hosted_zone(Id=id)

    def list_resource_record_sets(self, id):
        return self.client.list_resource_record_sets(HostedZoneId=id)

    def test_dns_answer(self, id, record_name, record_type):
        return self.client.test_dns_answer(
            HostedZoneId=id, RecordName=record_name, RecordType=record_type
        )


class HostedZone(object):
    id: str
    name: str

    def __init__(self, id, name):
        self.id = id
        self.name = name

    objects = Manager()

    @property
    def delegation_set(self):
        response = self.objects.client.get_hosted_zone(Id=self.id)
        return response.get("DelegationSet")
