from django.db import models
from django.utils.translation import ugettext_lazy as _

from nossas.design.models import UIBackgroundMixin, NamingPluginMixin, UICMSPlugin

class SocialSharePluginModel(UIBackgroundMixin, NamingPluginMixin, UICMSPlugin):
    title = models.CharField(max_length=255, verbose_name=_("Título"))

    def get_classes(self):
        classes = super().get_classes()

        color = self.attributes.get("color", "").replace("bg-", "text-")

        return classes + [color]
