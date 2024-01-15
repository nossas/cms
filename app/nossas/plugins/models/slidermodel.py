from django.db import models
from filer.fields.image import FilerImageField

from nossas.design.models import (
    UICMSPlugin,
    UIBackgroundMixin,
)


class FullPageSlider(UIBackgroundMixin, UICMSPlugin):
    background_image = FilerImageField(on_delete=models.SET_NULL, blank=True, null=True)
