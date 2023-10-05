from django.db import models

from cms.plugin_base import CMSPlugin

from colorfield.fields import ColorField

STYLED_COLOR_PALLETE = [
    (
        "#FFFFFF",
        "white",
    ),
    (
        "#000000",
        "black",
    ),
]

class Maps(CMSPlugin):
  geojson = models.FileField(upload_to="maps/geojson/")
  lineColor = ColorField(
      verbose_name="Cor da borda",
      samples=STYLED_COLOR_PALLETE,
      format="hexa",
      blank=True,
      null=True,
  )
  pointA = models.FileField(upload_to="maps/icons/")
  pointB = models.FileField(upload_to="maps/icons/")
