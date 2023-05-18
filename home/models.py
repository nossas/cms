from django.db import models
from django.utils.timezone import now

from wagtail import blocks
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel #, MultiFieldPanel, InlinePanel
from wagtail.images.blocks import ImageChooserBlock

from .blocks import PressureStructBlock, HeroStructBlock, SignatureStructBlock


class HomePage(Page):
    pass



class ThemeOptios(models.TextChoices):
    default = "css/default.css", "Default"
    custom = "css/custom.css", "Custom"


class ActionPage(Page):
    theme = models.CharField(
        verbose_name='Escolha seu tema',
        max_length=20,
        choices=ThemeOptios.choices,
        blank=True
    )
    created_date = models.DateField(default=now, editable=False)

    body = StreamField([
        ('hero', HeroStructBlock()),
        ('pressure', PressureStructBlock()),
        ('signature', SignatureStructBlock())
    ], block_counts={
        'hero': {'max_num': 1},
        'pressure': {'max_num': 1},
        'signature': {'max_num': 1},
    }, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('theme'),
        FieldPanel('body'),
    ]