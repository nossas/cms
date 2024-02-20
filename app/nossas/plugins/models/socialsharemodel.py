from django.db import models
from django.utils.translation import ugettext_lazy as _

from nossas.design.models import UIBackgroundMixin, NamingPluginMixin, UICMSPlugin

class SocialSharePluginModel(UIBackgroundMixin, NamingPluginMixin, UICMSPlugin):
    selected_social_media = models.CharField(max_length=255, blank=True, verbose_name="Redes Sociais Selecionadas")

    def get_selected_social_media_list(self):
        return self.selected_social_media.split(',') if self.selected_social_media else []

    def get_classes(self):
        classes = super().get_classes()

        color = self.attributes.get("color", "").replace("bg-", "text-")

        return classes + [color]
