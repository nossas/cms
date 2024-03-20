from django.db import models
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager


class OnSiteBaseModel(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    on_site = CurrentSiteManager()
    # Force objects queryset
    objects = CurrentSiteManager()

    class Meta:
        abstract = True
