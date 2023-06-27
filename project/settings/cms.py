# CMS Templates
# https://docs.django-cms.org/en/latest/how_to/install.html#templates

CMS_TEMPLATES = [
    # ("app/home.html", "Home"),
    ("frontend/landpage/page.html", "Landpage"),
]

# Placeholder
# https://docs.django-cms.org/en/latest/reference/configuration.html#std-setting-CMS_PLACEHOLDER_CONF
CMS_PLACEHOLDER_CONF = {
    "content": {
        "plugins": ["BlockPlugin", "BlockPressurePlugin"],
        "name": "Conteúdo",
    },
    "navigation": {
        "plugins": ["NavbarPlugin"],
        "language_fallback": True,
        "default_plugins": [
            {
                "plugin_type": "NavbarPlugin",
                "values": {}
            },
        ],
    },
    "footer": {
        "plugins": ["FooterPlugin"],
        "language_fallback": True,
        "default_plugins": [
            {
                "plugin_type": "FooterPlugin",
                "values": {}
            },
        ],
    },
}

# Picture
# https://github.com/django-cms/djangocms-picture

DJANGOCMS_PICTURE_ALIGN = [
    # Change prefix classes alignment for not use space
    (" object-left", "Esquerda"),
    (" mx-auto", "Centro"),
    (" object-right", "Direita"),
]

CMS_COLOR_SCHEME = "light"

CMS_COLOR_SCHEME_TOGGLE = False

from .ckeditor import *
