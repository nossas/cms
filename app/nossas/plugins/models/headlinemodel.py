from django.db import models
from cms.plugin_base import CMSPlugin


class HeadlineIconChoices(models.TextChoices):
    icon_rosa = "icon-rosa.svg", "Rosa"
    icon_azul = "icon-azul.svg", "Azul"
    icon_amarelo = "icon-amarelo.svg", "Amarelo"
    icon_laranja = "icon-laranja.svg", "Laranja"
    icon_verde = "icon-verde.svg", "Verde"
    icon_vermelho = "icon-vermelho.svg", "Vermelho"


class Headline(CMSPlugin):
    icon = models.CharField(
        choices=HeadlineIconChoices.choices, max_length=120, blank=True, null=True
    )

    @property
    def get_full_path_icon(self):
        return f"design/icons/{self.icon}"
