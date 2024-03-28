from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date

from filer.fields.image import FilerImageField

from nossas.apps.basemodel import OnSiteBaseModel


class TimelineEventContext(models.TextChoices):
    world = "mundo", _("Mundo")
    nossas = "nossas", _("Nossas")


class TimelineEvent(OnSiteBaseModel):
    event_context = models.CharField(choices=TimelineEventContext.choices, max_length=6, default=TimelineEventContext.world)
    day = models.IntegerField(_("Dia"), default=1)
    month = models.IntegerField(_("Mês"), default=1)
    year = models.IntegerField(_("Ano"), default=2024)
    title = models.CharField(_("Título"), max_length=140)
    # TODO: Contador de caracteres
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
        ordering = ["-year", "-month", "-day"]
        verbose_name = _("Evento da Timeline")
        verbose_name_plural = _("Eventos da Timeline")

    def get_event_date(self):
        return date(self.year, self.month, self.day)
