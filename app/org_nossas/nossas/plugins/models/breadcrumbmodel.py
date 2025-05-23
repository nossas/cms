from django.db import models
from django.utils.translation import gettext_lazy as _

from cms.plugin_base import CMSPlugin
from org_nossas.nossas.design.fields import GraphicIconCircleChoices


class Breadcrumb(CMSPlugin):
    graphic_icon = models.CharField(
        verbose_name=_("Ícone gráfico"),
        choices=GraphicIconCircleChoices.choices,
        max_length=50,
        blank=True,
        null=True,
    )
