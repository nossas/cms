from django.db import models
from django.utils.translation import gettext_lazy as _
from filer.fields.image import FilerImageField

from nossas.design.models import (
    UICMSPlugin,
    UIBackgroundMixin,
)


class FullPageSlider(UIBackgroundMixin, UICMSPlugin):
    background_image = FilerImageField(on_delete=models.SET_NULL, blank=True, null=True)
    x_and_y_center = models.BooleanField(
        verbose_name=_("Alinhar todo o conteúdo ao centro"), default=False
    )
