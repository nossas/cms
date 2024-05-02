from django.db import models
from django.contrib.sites.models import Site

from colorfield.widgets import ColorWidget
from django_jsonform.models.fields import JSONField

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
    "dark"
]

SCSS_SCHEMA = {
    "type": "dict",
    "keys": {
        "colors": {
            "type": "array",
            "items": {
                "type": "dict",
                "keys": {
                    "colorName": {"type": "string", "choices": COLORS},
                    "value": {"type": "string", "format": "color"},
                },
            },
        },
        "themeColors": {
            "type": "array",
            "items": {
                "type": "dict",
                "keys": {
                    "themeColorName": {"type": "string", "choices": THEME_COLORS},
                    "value": {"type": "string", "choices": COLORS}
                }
            }
        }
    },
}


class Theme(models.Model):
    scss_json = JSONField(schema=SCSS_SCHEMA, blank=True, null=True)
    site = models.OneToOneField(Site, primary_key=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Design System"

    def __str__(self):
        return self.site.name

    @property
    def scss(self):
        scss_text = ""

        # define colors
        colors = [
            f"${x['colorName']}: {x['value']};"
            for x in self.scss_json.get("colors", [])
        ]

        # define theme colors
        theme_colors = [
            f"${x['themeColorName']}: {x['value']};"
            for x in self.scss_json.get("themeColors", [])
        ]
        
        # merge colors
        scss_text += "\n".join(colors)
        # merge theme colors
        scss_text += "\n".join(theme_colors)
        
        print(scss_text)
        return scss_text
