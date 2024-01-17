from django.db import models
from cms.plugin_base import CMSPlugin


class Accordion(CMSPlugin):
    title = models.TextField(verbose_name="Título")
