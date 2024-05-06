from django.db import models

from cms.models import CMSPlugin
from filer.fields.file import FilerFileField


class Card(CMSPlugin):
    header_title = models.CharField(max_length=140, null=True, blank=True)
    image = FilerFileField(on_delete=models.SET_NULL, null=True, blank=True)
