from django.db import models

from cms.plugin_base import CMSPlugin
from filer.fields.image import FilerImageField
from colorfield.fields import ColorField

from contrib.frontend.models_styled import BlockElementStyled, STYLED_COLOR_PALLETE


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


class SpacingChoices(models.TextChoices):
    py_small = "py-12", "Pequeno"
    py_normal = "py-20", "Padrão"
    py_large = "py-28", "Grande"
    py_extra_large = "py-32", "Muito grande"


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

        return style if style != "" else None

    def classnames(self):
        classnames = ["container", "gap-8", "mx-auto", self.spacing]

        if self.alignment:
            classnames.append(self.alignment)

        return " ".join(classnames)


class Block(Section, Styled, CMSPlugin):
    class Meta:
        abstract = False


class Navbar(BlockElementStyled, CMSPlugin):
    class Meta:
        abstract = False
