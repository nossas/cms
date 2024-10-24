from django.db import models
from django.utils.translation import gettext_lazy as _

from filer.fields.file import FilerFileField


class Partner(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome da Parceria")
    logo = FilerFileField(verbose_name=_("Imagem"), on_delete=models.SET_NULL, null=True, blank=True)
    link = models.URLField(blank=True, null=True, verbose_name="Link da Parceria")

    position = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
        verbose_name="Posição"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Parceiro"
        ordering = ["position"]