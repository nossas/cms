from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPlugin

class SocialSharePluginModel(CMSPlugin):
    selected_social_media = models.CharField(max_length=255, blank=True, verbose_name=_("Selecione as redes sociais"))

    def get_selected_social_media_list(self):
        return self.selected_social_media.split(',') if self.selected_social_media else []
