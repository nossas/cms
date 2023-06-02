from django.db import models
from django.contrib.sites.models import Site


class GA(models.Model):
    uuid = models.CharField(
        "ID de métricas",
        help_text="Ex. G-XXXXXXXXXX",
        max_length=15,
        blank=True,
        null=True,
    )
    site = models.OneToOneField(Site, primary_key=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Google Analytics"

    def __str__(self):
        return self.site.name