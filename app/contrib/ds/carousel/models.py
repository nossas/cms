from django.db import models

from cms.models import CMSPlugin
from djangocms_text_ckeditor.fields import HTMLField


class CarouselContent(CMSPlugin):
    caption_html = HTMLField(null=True, blank=True)
