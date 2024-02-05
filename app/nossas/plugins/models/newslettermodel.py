from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPlugin


class NewsletterPluginModel(CMSPlugin):
    title = models.CharField(
        _("Título"),
        max_length=255,
        null=True,
        blank=True,
        default="Fique por dentro!",
    )
    description = models.TextField(_("Descrição"), null=True, blank=True)
    button_text = models.CharField(
        _("Texto do botão"),
        max_length=100,
        null=True,
        blank=True,
        default="Enviar",
    )
