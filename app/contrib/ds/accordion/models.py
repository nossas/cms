from django.db import models
from django.utils.translation import gettext_lazy as _

from cms.models import CMSPlugin
from colorfield.fields import ColorField

from contrib.ds.models import THEME_COLORS


class AccordionStyle(models.TextChoices):
    default = "", "default"
    flush = "flush", "flush"


class Accordion(CMSPlugin):
    style = models.CharField(
        verbose_name=_("Estilo"),
        max_length=7,
        choices=AccordionStyle.choices,
        default=AccordionStyle.default,
        blank=True,
    )
    grid_columns = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=_("Nº de Colunas"),
        help_text=_(
            "Use 0 para renderizar um item abaixo do outro sem espaçamento entre eles"
        ),
    )
    context = models.CharField(
        verbose_name=_("Cor de Contexto"),
        help_text=_("Define um padrão de Cor de Fundo e Cor de Texto"),
        max_length=30,
        choices=[(x, x) for x in THEME_COLORS],
        blank=True,
        null=True,
    )
    text_color = ColorField(
        verbose_name=_("Cor do Texto"),
        help_text=_("Sobrescreve o valor definido na Cor de Contexto"),
        null=True,
        blank=True,
    )
    bg_color = ColorField(
        verbose_name=_("Cor do Fundo"),
        help_text=_("Sobrescreve o valor definido na Cor de Contexto"),
        null=True,
        blank=True,
    )


class AccordionItem(CMSPlugin):
    header_title = models.CharField(max_length=140, null=True, blank=True)
