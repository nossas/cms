from django.db import models
from cms.plugin_base import CMSPlugin

layout_dict = {
    "g-col-12": 1,
    "g-col-12 g-col-md-6": 2,
    "g-col-12 g-col-md-4": 3,
    "g-col-12 g-col-md-3": 4,
    "g-col-12 g-col-md-2": 6,
    "g-col-12 g-col-md-1": 12,
}


class GridLayoutChoices(models.TextChoices):
    grid_auto = " ", "Auto"
    grid_1 = "g-col-12", "1 Coluna"
    grid_2 = "g-col-12 g-col-md-6", "2 Colunas"
    grid_3 = "g-col-12 g-col-md-4", "3 Colunas"
    grid_4 = "g-col-12 g-col-md-3", "4 Colunas"
    grid_6 = "g-col-12 g-col-md-2", "6 Colunas"
    grid_12 = "g-col-12 g-col-md-1", "12 Colunas"


class GridSpacingChoices(models.TextChoices):
    gap_0 = "row-gap: 0;", "Sem espaçamento"
    gap_4 = "row-gap: 4;", "Pequeno"
    gap_8 = "row-gap: 8;", "Grande"


class Grid(CMSPlugin):
    grid_layout = models.CharField(
        "Layout do Grid",
        max_length=80,
        default=GridLayoutChoices.grid_auto,
        choices=GridLayoutChoices.choices,
        help_text="Escolha 'Auto' para um layout responsivo automático ou para selecionar o número de colunas manualmente.",
    )
    grid_gap = models.CharField(
        "Espaçamento do Grid",
        default=GridSpacingChoices.gap_0,
        choices=GridSpacingChoices.choices,
        max_length=15,
        help_text="Selecione o espaço entre colunas do Grid.",
    )


class ColumnChoices(models.TextChoices):
    auto = " ", "Auto"
    col_1 = "g-col-1", "Col 1"
    col_2 = "g-col-2", "Col 2"
    col_3 = "g-col-3", "Col 3"
    col_4 = "g-col-4", "Col 4"
    col_5 = "g-col-5", "Col 5"
    col_6 = "g-col-6", "Col 6"
    col_7 = "g-col-7", "Col 7"
    col_8 = "g-col-8", "Col 8"
    col_9 = "g-col-9", "Col 9"
    col_10 = "g-col-10", "Col 10"
    col_11 = "g-col-11", "Col 11"
    col_12 = "g-col-12", "Col 12"


class RowChoices(models.TextChoices):
    auto = " ", "Auto"
    row_1 = "grid-row: 2", "Linha 2"
    row_2 = "grid-row: 3", "Linha 3"
    row_3 = "grid-row: 4", "Linha 4"


class ColumnStartAtChoices(models.TextChoices):
    auto = " ", "Auto"
    g_start_1 = "g-start-1", "Start at Col 1"
    g_start_2 = "g-start-2", "Start at Col 2"
    g_start_3 = "g-start-3", "Start at Col 3"
    g_start_4 = "g-start-4", "Start at Col 4"
    g_start_5 = "g-start-5", "Start at Col 5"
    g_start_6 = "g-start-6", "Start at Col 6"
    g_start_7 = "g-start-7", "Start at Col 7"
    g_start_8 = "g-start-8", "Start at Col 8"
    g_start_9 = "g-start-9", "Start at Col 9"
    g_start_10 = "g-start-10", "Start at Col 10"
    g_start_11 = "g-start-11", "Start at Col 11"
    g_start_12 = "g-start-12", "Start at Col 12"


class ColumnItemsSpacingChoices(models.TextChoices):
    gap_0 = "gap: 0;", "Sem espaçamento"
    gap_sm = "gap: 4px;", "Pequeno"
    gap_md = "gap: 6px;", "Médio"
    gap_lg = "gap: 8px;", "Grande"
    gap_xl = "gap: 12px;", "Muito Grande"


class YAlignmentChoices(models.TextChoices):
    left = "justify-content: flex-start;", "Acima"
    center = "justify-content: center;", "Ao centro"
    right = "justify-content: flex-end;", "Abaixo"


class XAlignmentChoices(models.TextChoices):
    start = "align-items: start;", "Esquerda"
    center = "align-items: center;", "Centralizar"
    end = "align-items: end;", "Direita"


class Column(CMSPlugin):
    col = models.CharField(
        "Coluna",
        choices=ColumnChoices.choices,
        default=ColumnChoices.auto,
        max_length=15,
        help_text="Defina manualmente o número de colunas que esta coluna ocupará.",
    )
    alignment_x = models.CharField(
        "Alinhamento horizontal",
        choices=XAlignmentChoices.choices,
        default=XAlignmentChoices.start,
        max_length=50,
    )
    alignment_y = models.CharField(
        "Alinhamento vertical",
        choices=YAlignmentChoices.choices,
        default=YAlignmentChoices.left,
        max_length=50,
    )
    spacing = models.CharField(
        "Espaçamento",
        choices=ColumnItemsSpacingChoices.choices,
        default=ColumnItemsSpacingChoices.gap_0,
        max_length=15,
        help_text="Selecione o espaçamento dos itens dentro da coluna.",
    )
    rows = models.CharField(
        "Linhas",
        choices=RowChoices.choices,
        default=RowChoices.auto,
        max_length=15,
        help_text="Escolha manualmente o número da linha que esta coluna ocupará.",
    )
    col_start_at = models.CharField(
        "Inicio da coluna na linha",
        choices=ColumnStartAtChoices.choices,
        default=ColumnStartAtChoices.auto,
        max_length=30,
        help_text="Defina em qual coluna o elemento deve iniciar.",
    )
