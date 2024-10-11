from django.db import models
from cms.models.fields import PlaceholderField

class StyleGuideModel(models.Model):
    name = models.CharField(verbose_name="Nome dos Plugins", max_length=120)
    placeholder = PlaceholderField("placeholder")

    def __str__(self):
      return self.name
