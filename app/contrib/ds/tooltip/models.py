from django.db import models
from django.utils.translation import gettext_lazy as _

from cms.models import CMSPlugin


class TooltipDirection(models.TextChoices):
    left = "", _("Esquerda")
    right = "right", _("Direita")


class Tooltip(CMSPlugin):
    direction = models.CharField(
        verbose_name=_("Direção"),
        max_length=30,
        null=True,
        blank=True,
        choices=TooltipDirection.choices,
    )
    message = models.TextField(verbose_name=_("Mensagem"))
