from django.db import models
from django.utils.translation import gettext_lazy as _

from filer.fields.image import FilerImageField
from translated_fields import TranslatedField
from org_nossas.nossas.apps.basemodel import OnSiteBaseModel


class MemberGroup(OnSiteBaseModel):
    name = TranslatedField(
        models.CharField(verbose_name=_("Nome da equipe"), max_length=120),
        {"en": {"blank": True}},
    )

    my_order = models.PositiveIntegerField(
        verbose_name=_("Posição"),
        default=0,
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = _("Equipe")
        ordering = ("my_order", "id")

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

    my_order = models.PositiveIntegerField(
        verbose_name=_("Posição"),
        default=0,
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = _("Colaborador")
        ordering = ("my_order", "full_name")
    
    def __str__(self):
        return self.short_name
