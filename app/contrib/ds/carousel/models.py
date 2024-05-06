from django.db import models

from cms.models import CMSPlugin
from djangocms_text_ckeditor.fields import HTMLField


class Carousel(CMSPlugin):
    enable_indicators = models.BooleanField(default=False)

class CarouselContent(CMSPlugin):
    caption_html = HTMLField(null=True, blank=True)
