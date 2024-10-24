from django.db import models
from django.utils.translation import gettext_lazy as _
from filer.fields.image import FilerImageField

from org_nossas.nossas.design.models import (
    UICMSPlugin,
    UIBackgroundMixin,
)


class BackgroundSize(models.TextChoices):
    contain = "contain"
    cover = "cover"
    initial = "initial"


class FullPageSlider(UIBackgroundMixin, UICMSPlugin):
    background_image = FilerImageField(on_delete=models.SET_NULL, blank=True, null=True)
    x_and_y_center = models.BooleanField(
        verbose_name=_("Alinhar todo o conteúdo ao centro"), default=False
    )
    background_size = models.CharField(
        choices=BackgroundSize.choices, max_length=8, default=BackgroundSize.contain
    )
