from django.db import models
from django.utils.translation import gettext_lazy as _

from filer.fields.image import FilerImageField

from nossas.apps.basemodel import OnSiteBaseModel


class TimelineEvent(OnSiteBaseModel):
    month = models.CharField(_("Mês"), max_length=20)
    year = models.IntegerField(_("Ano"))
    title = models.CharField(_("Título"), max_length=255)
    description = models.TextField(_("Descrição"))
    image = FilerImageField(
        related_name="timeline_images",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Imagem"))

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-year', '-month']
        verbose_name = _("Evento da Timeline")
        verbose_name_plural = _("Eventos da Timeline")
