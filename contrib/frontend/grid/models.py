from django.db import models

from cms.plugin_base import CMSPlugin


class XAlignmentChoices(models.TextChoices):
    center = "items-center", "Centro"
    start = "items-start", "Esquerda"
    end = "items-end", "Direita"

class YAlignmentChoices(models.TextChoices):
    start = "justify-start", "Acima"
    center = "justify-center", "Ao centro"
    end = "justify-end", "Abaixo"


class GridColumnChoices(models.TextChoices):
    grid_1 = "grid-cols-1", "1 Coluna"
    grid_2 = "grid-cols-1 md:grid-cols-2", "2 Colunas"
    grid_3 = "grid-cols-1 md:grid-cols-3", "3 Colunas"
    grid_4 = "grid-cols-1 sm:grid-cols-2 md:grid-cols-4", "4 Colunas"
    grid_1_2 = "grid-cols-1 md:grid-cols-[1fr_2fr]", "2 colunas, 4 x 8"


class Grid(CMSPlugin):
    cols = models.CharField(
        "Colunas",
        max_length=80,
        default=GridColumnChoices.grid_1,
        choices=GridColumnChoices.choices,
    )


class ColumnSpacingChoices(models.TextChoices):
    gap_0 = "gap-0", "Sem espaçamento"
    gap_4 = "gap-4", "Pequeno"
    gap_8 = "gap-8", "Grande"


class Column(CMSPlugin):
    spacing = models.CharField(
        "Espaçamento",
        choices=ColumnSpacingChoices.choices,
        default=ColumnSpacingChoices.gap_0,
        max_length=15,
        help_text="Espaço entre os elementos desta Coluna"
    )

    alignment_x = models.CharField(
        "Alinhamento Horizontal",
        choices=XAlignmentChoices.choices,
        default=XAlignmentChoices.center,
        max_length=30,
    )

    alignment_y = models.CharField(
        "Alinhamento Vertical",
        choices=YAlignmentChoices.choices,
        default=YAlignmentChoices.start,
        max_length=30
    )