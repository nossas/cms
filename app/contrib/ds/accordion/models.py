from django.db import models

from cms.models import CMSPlugin
from colorfield.fields import ColorField


class AccordionStyle(models.TextChoices):
    default = "", "default"
    flush = "flush", "flush"


class Accordion(CMSPlugin):
    style = models.CharField(
        max_length=7,
        choices=AccordionStyle.choices,
        default=AccordionStyle.default,
        blank=True,
    )
    grid_columns = models.PositiveSmallIntegerField(default=0)
    text_color = ColorField(null=True, blank=True)
    bg_color = ColorField(null=True, blank=True)


class AccordionItem(CMSPlugin):
    header_title = models.CharField(max_length=140, null=True, blank=True)
