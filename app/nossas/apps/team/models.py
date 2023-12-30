from django.db import models
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager

from filer.fields.image import FilerImageField
from translated_fields import TranslatedField


class MemberGroup(models.Model):
    name = TranslatedField(models.CharField(max_length=120), {"en": {"blank": True}})
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    on_site = CurrentSiteManager()

    def __str__(self):
        return self.name


class Member(models.Model):
    picture = FilerImageField(on_delete=models.SET_NULL, blank=True, null=True)
    short_name = models.CharField(max_length=80, blank=True, null=True)
    full_name = models.CharField(max_length=150)
    short_description = TranslatedField(
        models.CharField(max_length=255), {"en": {"blank": True}}
    )
    description = TranslatedField(models.TextField(), {"en": {"blank": True}})
    member_group = models.ForeignKey(
        MemberGroup, on_delete=models.SET_NULL, blank=True, null=True
    )
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    on_site = CurrentSiteManager()
