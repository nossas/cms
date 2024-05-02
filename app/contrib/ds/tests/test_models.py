# import pytest

from contrib.ds.models import Theme, DEFAULT_COLORS

colors_html = "\n".join([f"${color}: {value} !default;" for color, value in DEFAULT_COLORS.items()])

def test_define_base_colors():
    expected = "\n".join([f"${color}: {value} !default;" for color, value in ({
        **DEFAULT_COLORS,
        "blue": "#1f2dab",
        "green": "#1fab1f"
    }).items()])

    schema_json = {
        "colors": [
            {"colorName": "blue", "value": "#1f2dab"},
            {"colorName": "green", "value": "#1fab1f"},
        ]
    }

    theme = Theme(scss_json=schema_json)

    assert theme.scss == expected


def test_define_theme_colors():
    schema_json = {
        "themeColors": [
            {"themeColorName": "primary", "value": "green"},
            {"themeColorName": "secondary", "value": "yellow"},
        ]
    }

    theme = Theme(scss_json=schema_json)

    assert theme.scss == colors_html + '\n$primary: $green !default;\n$secondary: $yellow !default;'


def test_define_typography():
    schema_json = {
        "typography": {
            "heading": "Arial",
            "body": "Comic Sans"
        }
    }

    theme = Theme(scss_json=schema_json)

    assert theme.scss == colors_html + "\n$headings-font-family: Arial !default;\n$font-family-base: Comic Sans !default;"