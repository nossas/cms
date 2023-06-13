from django.db import models

from cms.plugin_base import CMSPlugin


class ColumnAlignChoices(models.TextChoices):
    items_center = "items-center", "Centro"
    items_left = "items-left", "Esquerda"
    items_right = "items-right", "Direita"


class ColumnChoices(models.TextChoices):
    grid_1 = "grid-cols-1", "1 Coluna"
    grid_2 = "grid-cols-1 md:grid-cols-2", "2 Colunas"
    grid_3 = "grid-cols-1 md:grid-cols-3", "3 Colunas"
    grid_4 = "grid-cols-1 sm:grid-cols-2 md:grid-cols-4", "4 Colunas"
    grid_1_2 = "grid-cols-1 md:grid-cols-[1fr_2fr]", "2 colunas, 4 x 8"


class Grid(CMSPlugin):
    cols = models.CharField(
        "Colunas",
        max_length=80,
        default=ColumnChoices.grid_1,
        choices=ColumnChoices.choices,
    )


class Column(CMSPlugin):
    align = models.CharField(
        "Alinhamento",
        choices=ColumnAlignChoices.choices,
        default=ColumnAlignChoices.items_center,
        max_length=30,
    )