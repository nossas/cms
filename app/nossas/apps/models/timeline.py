from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date

from filer.fields.image import FilerImageField

from nossas.apps.basemodel import OnSiteBaseModel


class TimelineEventContext(models.TextChoices):
    world = "mundo", _("Mundo")
    nossas = "nossas", _("Nossas")


class TimelineMonth(models.IntegerChoices):
    jan = 1, _("Janeiro")
    feb = 2, _("Fevereiro")
    mar = 3, _("Março")
    apr = 4, _("Abril")
    may = 5, _("Maio")
    jun = 6, _("Junho")
    jul = 7, _("Julho")
    aug = 8, _("Agosto")
    sep = 9, _("Setembro")
    oct = 10, _("Outubro")
    nov = 11, _("Novembro")
    dec = 12, _("Dezembro")


class TimelineEvent(OnSiteBaseModel):
    event_context = models.CharField(
        _("Contexto"),
        choices=TimelineEventContext.choices,
        max_length=6,
        default=TimelineEventContext.world,
    )
    day = models.IntegerField(_("Dia"), default=1)
    month = models.IntegerField(
        _("Mês"), default=TimelineMonth.jan, choices=TimelineMonth.choices
    )
    year = models.IntegerField(_("Ano"), default=2024)
    title = models.CharField(_("Título"), max_length=140)
    # TODO: Contador de caracteres
    description = models.TextField(_("Descrição"))
    image = FilerImageField(
        related_name="timeline_images",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Imagem"),
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-year", "-month", "-day"]
        verbose_name = _("Evento da Timeline")
        verbose_name_plural = _("Eventos da Timeline")

    def get_event_date(self):
        return date(self.year, self.month, self.day)
