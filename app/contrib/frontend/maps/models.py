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
  geojson = models.FileField(upload_to="maps/geojson/", blank=True, null=True)
  line_color = ColorField(
      verbose_name="Cor da linha",
      samples=STYLED_COLOR_PALLETE,
      format="hexa",
      blank=True,
      null=True,
  )
  point_a = models.FileField(upload_to="maps/icons/", blank=True, null=True)
  point_b = models.FileField(upload_to="maps/icons/", blank=True, null=True)
