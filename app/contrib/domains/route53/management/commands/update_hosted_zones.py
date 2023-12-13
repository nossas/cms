import boto3

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from contrib.domains.route53.models import HostedZone, RecordSet
from contrib.domains.route53.utils import get_record_set

# from route53.entries import HostedZone as HostedZoneEntry


class Command(BaseCommand):
    help = ""

    def get_list_resource_record_sets(self, hosted_zone_id, next_marker=None):
        params = {"Marker": next_marker} if next_marker else {}
        data = self.route53.list_resource_record_sets(
            HostedZoneId=hosted_zone_id, **params
        )

        yield self.prepare_record_set_list(data["ResourceRecordSets"])

        if data["IsTruncated"] == True and "NextMarker" in data.keys():
            yield from self.get_list_resource_record_sets(
                hosted_zone_id, next_marker=data["NextMarker"]
            )

    def get_list_hosted_zones(self, next_marker=None):
        params = {"Marker": next_marker} if next_marker else {}
        data = self.route53.list_hosted_zones(**params)

        yield self.prepare_hosted_zone_list(data["HostedZones"])

        if data["IsTruncated"] == True:
            # Chama função até não existir mais páginas
            yield from self.get_list_hosted_zones(next_marker=data["NextMarker"])

    def prepare_record_set_list(self, records=[]):
        return list(map(get_record_set, records))

    def prepare_hosted_zone_list(self, hosted_zones=[]):
        return list(
            map(
                lambda x: dict(id=x.get("Id", ""), name=x.get("Name", "")),
                hosted_zones,
            )
        )

    def handle(self, *args, **options):
        self.count = 0

        self.route53 = boto3.client(
            "route53",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            # aws_region=settings.AWS_REGION
        )

        # First called
        hosted_zones_next = self.get_list_hosted_zones()
        for hosted_zones in hosted_zones_next:
            for hosted_zone in hosted_zones:
                obj, created = HostedZone.objects.get_or_create(**hosted_zone)

                records_next = self.get_list_resource_record_sets(obj.id)
                for records in records_next:
                    for record in records:
                        obj, created = RecordSet.objects.get_or_create(
                            hosted_zone_id=hosted_zone["id"], **record
                        )

                if created:
                    self.count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully to create HostedZone: {self.count} objects."
            )
        )
