from django.db import models
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager

from filer.fields.image import FilerImageField
from translated_fields import TranslatedField


class CampaignStatus(models.TextChoices):
    opened = "opened", "Aberta"
    closed = "closed", "Fechada"


class Campaign(models.Model):
    name = models.CharField(max_length=180)
    description = TranslatedField(models.TextField(), {"en": {"blank": True}})
    picture = FilerImageField(on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=6, choices=CampaignStatus.choices)
    
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    on_site = CurrentSiteManager()

    def __str__(self):
        return self.name