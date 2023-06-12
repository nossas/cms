from django.db import models

from cms.models import CMSPlugin


class Email(CMSPlugin):
    subject = models.CharField(max_length=150)
    body = models.TextField()