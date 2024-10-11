from django.db import models

from cms.plugin_base import CMSPlugin
from filer.fields.file import FilerFileField


class PDFViewer(CMSPlugin):
    file = FilerFileField(on_delete=models.SET_NULL, null=True, blank=True)
