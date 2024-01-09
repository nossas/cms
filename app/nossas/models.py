from django.db import models
from cms.models.fields import PlaceholderField

class StyleGuideModel(models.Model):
  name = models.CharField(verbose_name="Nome dos Plugins", max_length=120)
  placeholder = PlaceholderField("placeholder")
  css_classes = models.CharField(verbose_name="Classes CSS", max_length=120, blank=True, null=True)

  def __str__(self):
    return self.name
