from django.db import models

from colorfield.fields import ColorField

from project.settings.ckeditor.font import font_family_options


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