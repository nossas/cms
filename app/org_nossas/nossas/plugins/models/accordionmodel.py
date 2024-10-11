from django.db import models
from cms.plugin_base import CMSPlugin


class AccordionItem(CMSPlugin):
    title = models.TextField(verbose_name="Título do Acordeon")
