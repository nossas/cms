from django.db import models


from filer.fields.image import FilerImageField
from translated_fields import TranslatedField
from nossas.apps.basemodel import OnSiteBaseModel


class MemberGroup(OnSiteBaseModel):
    name = TranslatedField(models.CharField(max_length=120), {"en": {"blank": True}})

    def __str__(self):
        return self.name


class Member(OnSiteBaseModel):
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
