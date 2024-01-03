from django import template
from django.conf import settings
from django.utils.text import slugify
from django.utils.safestring import mark_safe

register = template.Library()


# scss_text = """
# $utilities: map-merge(
#     $utilities,
#     (
#         "background-color": (
#             property: background-color,
#             class: bg,
#             values:
#                 map-merge(
#                     $theme-colors,
#                     (
# {{COLORS}}
#                     )
#                 )
#         ),
#         "color": (
#             property: color,
#             class: text,
#             values:
#                 map-merge(
#                     $utilities-text-colors,
#                     (
# {{COLORS}}
#                     )
#                 )
#         )
#     )
# );
# """
scss_text = """
// Create your own map
$custom-colors: (
    {{COLORS}}
);

{{VARIABLES}}

// Merge the maps
$theme-colors: map-merge($theme-colors, $custom-colors);

// Create constrast
@each $color, $value in $theme-colors {
    .bg-#{$color}, .tag-#{$color} {
        background-color: $value;
        color: color-contrast($value);
    }
    .btn-#{$color} {
        color: color-contrast($value);
    }
    .text-#{$color} {
        color: $value;

        &.btn {
            color: $value;

            &:hover {
                color: $value;
            }
        }
    }
}
"""


@register.simple_tag
def build_colors():
    if hasattr(settings, "DESIGN_THEME_COLORS"):
        COLORS = ",".join(
            [f'"{slugify(args[0])}":{args[1]}' for args in settings.DESIGN_THEME_COLORS]
        )

        TEXT_COLORS = ";".join(
            [
                f'$text-{slugify(args[0])}-emphasis:{args[1]}'
                for args in settings.DESIGN_THEME_TEXT_COLORS
            ]
        )

        print(TEXT_COLORS)
        return mark_safe(
            scss_text.replace("{{COLORS}}", COLORS).replace(
                "{{VARIABLES}}", TEXT_COLORS + ";"
            )
        )

    return ""
