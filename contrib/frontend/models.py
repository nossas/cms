from django.db import models

from cms.plugin_base import CMSPlugin
from filer.fields.image import FilerImageField
from colorfield.fields import ColorField

from project.settings.ckeditor.font import font_family_options


class Section(models.Model):
    title = models.CharField("título", max_length=80, blank=True)

    slug = models.SlugField(
        verbose_name="slug",
        max_length=80,
        blank=True,
        help_text="a parte do título que é usada na URL",
    )

    menu_title = models.CharField(
        "título do menu",
        help_text="padrão é igual ao título do bloco",
        max_length=50,
        blank=True,
    )

    menu_hidden = models.BooleanField("esconder menu?", default=False)

    hidden = models.BooleanField("esconder bloco?", default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def get_menu_title(self):
        return self.menu_title or self.title


STYLED_COLOR_PALLETE = [
    (
        "#FFFFFF",
        "white",
    ),
    (
        "#000000",
        "black",
    ),
]


class Styled(models.Model):
    spacing = models.CharField("margem", max_length=30, default="py-7")

    background_color = ColorField(
        samples=STYLED_COLOR_PALLETE, format="hexa", blank=True, null=True
    )

    background_image = FilerImageField(
        verbose_name="Imagem de fundo", blank=True, null=True, on_delete=models.SET_NULL
    )

    class Meta:
        abstract = True

    def get_background_css(self):
        # import ipdb;ipdb.set_trace()
        return "bg-[#FF2269FF]"

    def styles(self):
        style = ""

        if self.background_image:
            style += f"background: url({self.background_image.url}) no-repeat;background-size:cover;"

        if self.background_color and not self.background_image:
            style += f"background-color:{self.background_color};"

        if self.background_color and self.background_image:
            style += f"box-shadow: inset 0 0 0 1000px {self.background_color}"

        return style


class LayoutChoices(models.TextChoices):
    hero = "hero", "Hero"
    hero_nobrand = "hero_nobrand", "Hero Sem logo"
    tree_columns = "tree_columns", "3 Colunas"
    four_columns = "four_columns", "4 Colunas"
    two_columns_a = "two_columns_a", "2 Colunas - 6x6"
    two_columns_b = "two_columns_b", "2 Colunas - 4x8"
    signature = "signature", "Assinatura"
    signature_partners_a = (
        "signature_partners_a",
        "2 Colunas - Assinatura com parceiros",
    )
    signature_partners_b = "signature_partners_b", "1 Coluna - Assinatura com parceiros"


class Block(Section, Styled, CMSPlugin):
    layout = models.CharField(
        "Layout", choices=LayoutChoices.choices, max_length=75, blank=True, null=True
    )


class AlignChoices(models.TextChoices):
    items_center = "justify-items-center", "Centro"
    items_left = "justify-items-left", "Esquerda"
    items_right = "justify-items-right", "Direita"


class ColumnChoices(models.TextChoices):
    grid_1 = "grid-cols-1", "1 Coluna"
    grid_2 = "grid-cols-1 md:grid-cols-2", "2 Colunas"
    grid_3 = "grid-cols-1 md:grid-cols-3", "3 Colunas"
    grid_4 = "grid-cols-1 sm:grid-cols-2 md:grid-cols-4", "4 Colunas"
    grid_1_2 = "grid-cols-1 md:grid-cols-[1fr_2fr]" , "2 colunas, 4 x 8"


class Grid(CMSPlugin):
    cols = models.CharField(
        "Colunas",
        max_length=80,
        default=ColumnChoices.grid_1,
        choices=ColumnChoices.choices,
    )
    align = models.CharField(
        "Alinhamento",
        choices=AlignChoices.choices,
        default=AlignChoices.items_center,
        max_length=30,
    )


class Navbar(CMSPlugin):
    font = models.CharField(
        "Estilo de fonte",
        choices=list(map(lambda x: (x, x), font_family_options)),
        max_length=100,
        blank=True,
        null=True
    )
    color = ColorField(
        verbose_name="Cor da fonte",
        samples=STYLED_COLOR_PALLETE,
        format="hexa",
        blank=True,
        null=True,
    )
    background_color = ColorField(
        verbose_name="Cor de fundo",
        samples=STYLED_COLOR_PALLETE,
        format="hexa",
        blank=True,
        null=True,
    )

    def styles(self):
        styles = ""

        if self.font:
            styles += f"font-family:{self.font};"
        
        if self.background_color:
            styles += f"background-color:{self.background_color};"
        
        if self.color:
            styles += f"color:{self.color};"
        
        return styles if len(styles) > 0 else None
        