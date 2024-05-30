from django.db import models
from cms.models.pluginmodel import CMSPlugin

class MapPlugin(CMSPlugin):
    url = models.URLField("URL do mapa")
    width = models.CharField("Largura", max_length=10, default="100%")
    height = models.CharField("Altura", max_length=10, default="100%")