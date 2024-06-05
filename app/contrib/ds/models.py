from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.models import Site
from django.utils.html import mark_safe

from cms.models import CMSPlugin
from colorfield.fields import ColorField
from django_jsonform.models.fields import JSONField
from filer.fields.image import FilerImageField

DEFAULT_COLORS = {
    "blue": "#0d6efd",
    "indigo": "#6610f2",
    "purple": "#6f42c1",
    "pink": "#d63384",
    "red": "#dc3545",
    "orange": "#fd7e14",
    "yellow": "#ffc107",
    "green": "#198754",
    "teal": "#20c997",
    "cyan": "#0dcaf0",
    "black": "#000",
    "white": "#fff",
}

COLORS = [
    "blue",
    "indigo",
    "purple",
    "pink",
    "red",
    "orange",
    "yellow",
    "green",
    "teal",
    "cyan",
    "gray",
    "black",
    "white",
]

THEME_COLORS = [
    "primary",
    "secondary",
    "success",
    "danger",
    "warning",
    "info",
    "light",
    "dark",
]

FONT_FAMILIES = [
    "Abel",
    "Anton",
    "Archivo Narrow",
    "Arvo",
    "Asap",
    "Avenir Next LT Pro",
    "Baloo Bhai",
    "Bebas Neue Pro",
    "Bitter",
    "Bree Serif",
    "Capriola",
    "Cabin",
    "Catamaran",
    "Crimson Text",
    "Cuprum",
    "David Libre",
    "Dosis",
    "Droid Sans",
    "Exo",
    "Exo 2",
    "Fira Sans",
    "Fjalla One",
    "Francois One",
    "Gidugu",
    "Hind",
    "Inconsolata",
    "Indie Flower",
    "Josefin Sans",
    "Karla",
    "Lalezar",
    "Lato",
    "Libre Baskerville",
    "Linear Grotesk",
    "Lobster",
    "Lora",
    "Merriweather Sans",
    "Montserrat",
    "Muli",
    "Noto Serif",
    "Nunito Sans",
    "Open Sans",
    "Open Sans Condensed",
    "Oswald",
    "Oxygen",
    "PT Sans",
    "PT Serif",
    "Pacifico",
    "Playfair Display",
    "Poiret One",
    "Poppins",
    "Quicksand",
    "Raleway",
    "Roboto",
    "Roboto Condensed",
    "Roboto Mono",
    "Roboto Slab",
    "Ruslan Display",
    "Signika",
    "Slabo 27px",
    "Source Sans Pro",
    "Titillium Web",
    "Ubuntu",
    "Ubuntu Condensed",
    "Varela Round",
    "Yanone Kaffeesatz",
]

SCSS_SCHEMA = {
    "type": "dict",
    "keys": {
        "typography": {
            "type": "dict",
            "keys": {
                "heading": {
                    "type": "string",
                    "choices": FONT_FAMILIES,
                    "required": False,
                },
                "body": {"type": "string", "choices": FONT_FAMILIES, "required": False},
            },
            "required": False,
        },
        "colors": {
            "type": "array",
            "items": {
                "type": "dict",
                "keys": {
                    "colorName": {"type": "string", "choices": COLORS},
                    "value": {"type": "string", "format": "color"},
                },
            },
            "required": False,
        },
        "themeColors": {
            "type": "array",
            "items": {
                "type": "dict",
                "keys": {
                    "themeColorName": {"type": "string", "choices": THEME_COLORS},
                    "value": {"type": "string", "choices": COLORS},
                },
            },
            "required": False,
        },
    },
}


class Theme(models.Model):
    scss_json = JSONField(schema=SCSS_SCHEMA, blank=True, null=True)

    favicon = FilerImageField(
        verbose_name=_("Favicon"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    site = models.OneToOneField(Site, primary_key=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Design System")

    def __str__(self):
        return self.site.name

    @property
    def scss(self):
        scss_text = ""

        # define colors
        colors = {}
        for x in self.scss_json.get("colors", []):
            colors[x.get("colorName")] = x.get("value")

        colors = {**DEFAULT_COLORS, **colors}

        scss_text += "\n".join(
            [
                f"${colorName}: {colors[colorName]} !default;"
                for colorName in colors.keys()
            ]
        )

        # define theme colors
        theme_colors = [
            f"${x['themeColorName']}: ${x['value']} !default;"
            for x in self.scss_json.get("themeColors", [])
        ]

        # merge theme colors
        if len(theme_colors) > 0:
            scss_text += "\n" + "\n".join(theme_colors)

        # typography
        typography = self.scss_json.get("typography", {})
        if typography.get("heading"):
            scss_text += (
                "\n"
                + "$headings-font-family: "
                + typography.get("heading")
                + " !default;"
            )

        if typography.get("body"):
            scss_text += (
                "\n" + "$font-family-base: " + typography.get("body") + " !default;"
            )

        return mark_safe(scss_text)


class SEO(models.Model):
    title = models.CharField(
        verbose_name=_("Título"),
        help_text=_("Limite de 60 caracteres"),
        max_length=60,
        null=True,
        blank=True,
    )
    description = models.CharField(
        verbose_name=_("Descrição"),
        help_text=_("Limite de 155 caracteres"),
        max_length=155,
        null=True,
        blank=True,
    )
    image = FilerImageField(
        verbose_name=_("Imagem de compartilhamento"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    site = models.OneToOneField(Site, primary_key=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Metadados SEO")


class NavbarAlignment(models.TextChoices):
    start = "", "start"
    center = "center", "center"
    end = "flex-end", "end"


class NavbarPlacement(models.TextChoices):
    default = "", "default"
    fixed = "fixed-top", "fixed"
    sticky = "sticky-top", "sticky"


class Navbar(CMSPlugin):
    brand = FilerImageField(on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=120, null=True, blank=True)
    context = models.CharField(
        max_length=30, choices=[(x, x) for x in THEME_COLORS], null=True, blank=True
    )
    alignment = models.CharField(
        max_length=30, choices=NavbarAlignment.choices, null=True, blank=True
    )
    placement = models.CharField(
        max_length=30, choices=NavbarPlacement.choices, null=True, blank=True
    )


class ActiveStyled(models.TextChoices):
    default = "", "default"
    underline = "underline", "underline"


class Menu(CMSPlugin):
    color = ColorField(null=True, blank=True)
    active_styled = models.CharField(
        max_length=30, choices=ActiveStyled.choices, null=True, blank=True
    )
