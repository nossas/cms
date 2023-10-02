from django.db import models

from cms.plugin_base import CMSPlugin

class Maps(CMSPlugin):
  geojson = models.FileField(upload_to="maps/geojson/")