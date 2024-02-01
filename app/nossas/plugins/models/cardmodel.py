from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.plugin_base import CMSPlugin
from filer.fields.file import FilerFileField

from nossas.design.models import NamingPluginMixin


class Card(NamingPluginMixin, CMSPlugin):
    image = FilerFileField(verbose_name=_("Imagem"), on_delete=models.SET_NULL, null=True, blank=True)
    tag = models.CharField(verbose_name=_("Tag"), max_length=50, null=True, blank=True)
