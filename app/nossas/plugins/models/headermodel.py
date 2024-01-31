from django.db import models
from django.utils.translation import ugettext_lazy as _

from filer.fields.image import FilerImageField

from nossas.design.fields import GraphicElementChoices
from nossas.design.models import UICMSPlugin, UIBackgroundMixin, NamingPluginMixin


class Header(UIBackgroundMixin, NamingPluginMixin, UICMSPlugin):
    graphic_element = models.CharField(
        verbose_name=_("Elemento gráfico"),
        choices=GraphicElementChoices.choices,
        max_length=120,
        blank=True,
        null=True,
    )
