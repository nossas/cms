from django.db import models
from django.utils.translation import gettext_lazy as _

from filer.fields.image import FilerImageField
from translated_fields import TranslatedField
from nossas.apps.basemodel import OnSiteBaseModel


class MemberGroup(OnSiteBaseModel):
    name = TranslatedField(
        models.CharField(verbose_name=_("Nome da equipe"), max_length=120),
        {"en": {"blank": True}},
    )

    class Meta:
        verbose_name = _("Equipe")

    def __str__(self):
        return self.name


class Member(OnSiteBaseModel):
    picture = FilerImageField(
        verbose_name=_("Foto"), on_delete=models.SET_NULL, blank=True, null=True
    )
    short_name = models.CharField(
        verbose_name=_("Nome"), max_length=80, blank=True, null=True
    )
    full_name = models.CharField(verbose_name=_("Nome completo"), max_length=150)
    short_description = TranslatedField(
        models.CharField(verbose_name=_("Descrição curta"), max_length=255),
        {"en": {"blank": True}},
    )
    description = TranslatedField(
        models.TextField(verbose_name=_("Descrição completa")), {"en": {"blank": True}}
    )
    member_group = models.ForeignKey(
        MemberGroup,
        verbose_name=_("Equipe"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Colaborador")
    
    def __str__(self):
        return self.short_name
