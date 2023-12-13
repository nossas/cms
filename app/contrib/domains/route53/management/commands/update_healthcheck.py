import boto3

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from contrib.domains.route53.models import HostedZone, RecordSet


class Command(BaseCommand):
    help = ""

    def handle(self, *args, **options):
        for hz in HostedZone.objects.all():
            hz.healtcheck = hz.check_ns()
            hz.save()

        is_ok = HostedZone.objects.filter(healtcheck=True).count()
        is_fail = HostedZone.objects.filter(healtcheck=False).count()

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully to update HostedZone: {is_ok} ok | {is_fail} fail."
            )
        )
