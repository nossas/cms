from django.db import models

from cms.extensions import PageExtension
from cms.extensions.extension_pool import extension_pool
from filer.fields.image import FilerImageField


class IconExtension(PageExtension):
    favicon = FilerImageField(
        verbose_name="Favicon",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )


extension_pool.register(IconExtension)


class MetaDataExtension(PageExtension):
    image = FilerImageField(
        verbose_name="Thumbnail",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    title = models.CharField(
        verbose_name="Título da postagem",
        blank=True,
        null=True,
        max_length=70
    )
    subtitle = models.CharField(
        verbose_name="Texto da postagem",
        blank=True,
        null=True,
        max_length=90
    )

extension_pool.register(MetaDataExtension)
