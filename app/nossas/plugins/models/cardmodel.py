from django.db import models
from cms.plugin_base import CMSPlugin
from filer.fields.file import FilerFileField

from nossas.design.models import NamingPluginMixin


class Card(NamingPluginMixin, CMSPlugin):
    image = FilerFileField(on_delete=models.SET_NULL, null=True, blank=True)
    tag = models.CharField(max_length=20, null=True, blank=True)
