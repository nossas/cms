from django.db import models
from django.utils.translation import gettext_lazy as _

from cms.plugin_base import CMSPlugin
from filer.fields.image import FilerImageField

from org_nossas.nossas.design.fields import GraphicElementChoices, GraphicIconChoices
from org_nossas.nossas.design.models import UICMSPlugin, UIBackgroundMixin, NamingPluginMixin


class Header(UIBackgroundMixin, NamingPluginMixin, UICMSPlugin):
    graphic_element = models.CharField(
        verbose_name=_("Elemento gráfico"),
        choices=GraphicElementChoices.choices,
        max_length=120,
        blank=True,
        null=True,
    )


class HeaderImage(CMSPlugin):
    graphic_icon = models.CharField(
        verbose_name=_("Ícone gráfico"),
        choices=GraphicIconChoices.choices,
        max_length=50,
        blank=True,
        null=True,
    )

    picture = FilerImageField(
        verbose_name=_("Imagem de Fundo"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
