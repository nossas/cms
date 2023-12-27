from django import template
from django.conf import settings
from django.utils.text import slugify
from django.utils.safestring import mark_safe

register = template.Library()


scss_text = """
$utilities: map-merge(
    $utilities,
    (
        "background-color": (
            property: background-color,
            class: bg,
            values:
                map-merge(
                    $theme-colors,
                    (
{{COLORS}}
                    )
                )
        ),
        "color": (
            property: color,
            class: text,
            values:
                map-merge(
                    $utilities-text-colors,
                    (
{{COLORS}}
                    )
                )
        )
    )
);
"""

@register.simple_tag
def build_colors():
    if hasattr(settings, "DESIGN_THEME_COLORS"):
        COLORS = ",".join([
            f'"{slugify(args[0])}":{args[1]}' for args in settings.DESIGN_THEME_COLORS
        ])

        return mark_safe(scss_text.replace("{{COLORS}}", COLORS))
    
    return ""