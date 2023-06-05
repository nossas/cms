from django.db import models

from cms.models import CMSPlugin


class Pressure(CMSPlugin):
    widget = models.IntegerField(null=True, blank=True)