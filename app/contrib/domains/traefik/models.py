from django.conf import settings
from django.db import models
from etcd3 import Client

from contrib.domains.route53.models import HostedZone, RecordSet, VPS, RecordType


class Container(models.TextChoices):
    webpage = "webpage@docker", "Public"
    djangocms = "cms@docker", "CMS"


class Route(models.Model):
    dns = models.ForeignKey(HostedZone, on_delete=models.CASCADE)
    subdomain = models.ForeignKey(
        RecordSet,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"record_type": RecordType.A},
    )
    instance = models.ForeignKey(VPS, on_delete=models.SET_NULL, null=True, blank=True)
    service = models.CharField(max_length=25, choices=Container.choices)

    def get_traefik_config(self):
        domain = (
            self.subdomain.name
            if self.subdomain.name[-1] != "."
            else self.subdomain.name[:-1]
        )
        prefix = f"traefik/http/routers/{self.id}-{domain.replace('.', '-')}"

        configs = (
            ("/tls", "true"),
            ("/tls/certresolver", "myresolver"),
            ("/service", self.service),
            (
                "/rule",
                "HostRegexp(`DOMAIN_NAME`, `{subdomain:.+}.DOMAIN_NAME`)".replace(
                    "DOMAIN_NAME", domain
                ),
            ),
            ("/tls/domains/0/main", domain),
            ("/tls/domains/0/sans/0", "*." + domain),
        )

        return list(map(lambda x: (prefix + x[0], x[1]), configs))

    def update_traefik_config(self):
        try:
            client = Client(host=settings.ETCD_HOST, port=settings.ETCD_PORT)

            for config in self.get_traefik_config():
                client.put(key=config[0], value=config[1])

            return True
        except Exception:
            return False

    def delete_traefik_config(self):
        try:
            client = Client(host=settings.ETCD_HOST, port=settings.ETCD_PORT)
    
            for config in self.get_traefik_config():
                client.delete_range(key=config[0])
            
            return True
        except Exception:
            return False