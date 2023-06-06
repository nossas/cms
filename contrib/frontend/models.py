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


class SpacingChoices(models.TextChoices):
    py_extra_small = "py-8", "Extra small"
    py_small = "py-10", "Small"
    py_normal = "py-12", "Default"
    py_large = "py-14", "Large"
    py_extra_large = "py-16", "Extra large"


class AlignmentChoices(models.TextChoices):
    center = "grid justify-items-center", "Centralizar"
    left = "grid justify-items-start", "Esquerda"
    right = "grid justify-items-end", "Direita"


class Styled(models.Model):
    spacing = models.CharField(
        "espaçamento",
        max_length=30,
        choices=SpacingChoices.choices,
        default=SpacingChoices.py_normal,
    )
    alignment = models.CharField(
        "alinhamento",
        max_length=30,
        choices=AlignmentChoices.choices,
        blank=True,
        null=True,
        default=AlignmentChoices.left,
    )

    background_color = ColorField(
        samples=STYLED_COLOR_PALLETE, format="hexa", blank=True, null=True
    )

    background_image = FilerImageField(
        verbose_name="Imagem de fundo", blank=True, null=True, on_delete=models.SET_NULL
    )

    class Meta:
        abstract = True

    def styles(self):
        style = ""

        if self.background_image:
            style += f"background: url({self.background_image.url}) no-repeat;background-size:cover;"

        if self.background_color and not self.background_image:
            style += f"background-color:{self.background_color};"

        if self.background_color and self.background_image:
            style += f"box-shadow: inset 0 0 0 1000px {self.background_color}"

        return style

    def classnames(self):
        classnames = ["container", "gap-4", "mx-auto", self.spacing]

        if self.alignment:
            classnames.append(self.alignment)

        return " ".join(classnames)


class Block(Section, Styled, CMSPlugin):
    class Meta:
        abstract = False


class AlignChoices(models.TextChoices):
    items_center = "justify-items-center", "Centro"
    items_left = "justify-items-left", "Esquerda"
    items_right = "justify-items-right", "Direita"


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
    align = models.CharField(
        "Alinhamento",
        choices=AlignChoices.choices,
        default=AlignChoices.items_center,
        max_length=30,
    )



class BlockElementStyled(models.Model):
    font = models.CharField(
        "Estilo de fonte",
        choices=list(map(lambda x: (x, x), font_family_options)),
        max_length=100,
        blank=True,
        null=True,
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

    class Meta:
        abstract = True

    def styles(self):
        styles = ""

        if self.font:
            styles += f"font-family:{self.font};"

        if self.background_color:
            styles += f"background-color:{self.background_color};"

        if self.color:
            styles += f"color:{self.color};"

        return styles if len(styles) > 0 else None


class Navbar(BlockElementStyled, CMSPlugin):
    class Meta:
        abstract = False


class BorderSizeChoices(models.TextChoices):
    border = "border", "Padrão (1px)"
    border_0 = "border-0", "Sem borda (0px)"
    border_2 = "border-2", "Pequeno (2px)"
    border_4 = "border-4", "Médio (4px)"
    border_8 = "border-8", "Grande (8px)"


class RoundedChoices(models.TextChoices):
    none = "rounded-none", "Sem arredondamento"
    sm = "rounded-sm", "Small"
    md = "rounded-md", "Medium"
    lg = "rounded-lg", "Large"
    xl = "rounded-xl", "Extra Large"


class Button(BlockElementStyled, CMSPlugin):
    title = models.CharField("Título", max_length=80)
    action_url = models.CharField(
        "endereço da ação", max_length=200, help_text="slug do bloco usado na URL"
    )
    target_blank = models.BooleanField(verbose_name="Abrir em nova aba?", default=False)
    bold = models.BooleanField(verbose_name="Negrito?", default=False)
    border_color = ColorField(
        verbose_name="Cor da borda",
        samples=STYLED_COLOR_PALLETE,
        format="hexa",
        blank=True,
        null=True,
    )
    border_size = models.CharField(
        verbose_name="Tamanho da borda",
        choices=BorderSizeChoices.choices,
        max_length=30,
        blank=True,
        null=True,
    )
    rounded = models.CharField(
        verbose_name="Arredondamento",
        choices=RoundedChoices.choices,
        max_length=30,
        blank=True,
        null=True,
    )

    def styles(self):
        styles = super(Button, self).styles()

        if self.background_color and not self.border_color:
            styles += f"border-color:{self.background_color};"

        return styles


class KindChoices(models.TextChoices):
    twitter = "twitter", "Twitter"
    facebook = "facebook", "Facebook"
    instagram = "instagram", "Instagram"
    site = "site", "Site"


class SocialMedia(CMSPlugin):
    def copy_relations(self, oldinstance):
        self.socialmediaitem_set.all().delete()

        for item in oldinstance.socialmediaitem_set.all():
            item.pk = None
            item.plugin = self
            item.save()


class SocialMediaItem(models.Model):
    url = models.CharField(
        verbose_name="URL",
        max_length=100,
    )
    kind = models.CharField(
        verbose_name="Tipo",
        max_length=100,
        choices=KindChoices.choices,
    )
    icon = FilerImageField(
        verbose_name="Ícone", blank=True, null=True, on_delete=models.SET_NULL
    )
    plugin = models.ForeignKey(SocialMedia, on_delete=models.CASCADE)
