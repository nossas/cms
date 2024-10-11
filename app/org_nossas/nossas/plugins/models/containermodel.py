from django.db import models
from django.utils.translation import gettext_lazy as _

from org_nossas.nossas.design.models import (
    UICMSPlugin,
    UIBackgroundMixin,
    UIPaddingMixin,
    UIBorderMixin,
    NamingPluginMixin,
)


class Container(
    UIBackgroundMixin, UIPaddingMixin, UIBorderMixin, NamingPluginMixin, UICMSPlugin
):
    fluid = models.BooleanField(
        verbose_name=_("Conteúdo fluído"),
        default=False,
        help_text=_("Permite o conteúdo interno avançar os limites padrões da página"),
    )
