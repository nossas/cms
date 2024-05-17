from django.db import models

from cms.models import CMSPlugin


class Tooltip(CMSPlugin):
    direction = models.CharField(max_length=30, null=True, blank=True)
    message = models.TextField()
