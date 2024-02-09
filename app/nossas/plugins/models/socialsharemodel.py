from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin


class SocialSharePluginModel(CMSPlugin):
    title = models.CharField(max_length=255, verbose_name=_("Título"))
