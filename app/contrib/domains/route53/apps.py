from django.apps import AppConfig
from django.db.models.signals import pre_delete, pre_save


class Route53AppConfig(AppConfig):
    name = "contrib.domains.route53"

    def ready(self):
        from . import signals, models

        # pre_save.connect(signals.create_or_update_route53, models.HostedZone)

        pre_delete.connect(signals.delete_on_route53, models.RecordSet)
        pre_delete.connect(signals.delete_on_route53, models.HostedZone)
