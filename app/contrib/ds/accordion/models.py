from django.db import models

from cms.models import CMSPlugin


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


class AccordionItem(CMSPlugin):
    header_title = models.CharField(max_length=140, null=True, blank=True)
