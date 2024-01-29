from django.db import models
from django.utils.translation import ugettext_lazy as _

from filer.fields.image import FilerImageField

from nossas.design.models import UICMSPlugin, UIBackgroundMixin, NamingPluginMixin


class Header(UIBackgroundMixin, NamingPluginMixin, UICMSPlugin):
    picture = FilerImageField(
        verbose_name=_("Imagem"), on_delete=models.SET_NULL, blank=True, null=True
    )
