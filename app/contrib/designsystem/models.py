from django.db import models
from django.contrib.sites.models import Site


class ThemeScss(models.Model):
    theme = models.TextField(
        verbose_name="Tema", null=True, blank=True
    )
    site = models.OneToOneField(Site, primary_key=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Theme Scss"
