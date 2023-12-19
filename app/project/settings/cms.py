# CMS Templates
# https://docs.django-cms.org/en/latest/how_to/install.html#templates

CMS_TEMPLATES = [
    # ("app/home.html", "Home"),
    ("frontend/landpage/page.html", "Landpage"),
    ("eleicao/eleicao_template.html", "A Eleição do Ano"),
    ("designsystem/base.html", "Design System"),
]

# Placeholder
# https://docs.django-cms.org/en/latest/reference/configuration.html#std-setting-CMS_PLACEHOLDER_CONF
CMS_PLACEHOLDER_CONF = {
    "content": {
        "name": "Blocos",
        "plugins": ["BlockPlugin", "BlockPressurePlugin", "EleicaoCandidateListPlugin", "EleicaoCarouselPlugin", "EleicaoVoterFormPlugin"],
    },
    "navigation": {
        "name": "Navegação",
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
        "name": "Rodapé",
        "plugins": ["FooterPlugin"],
        "language_fallback": True,
        "default_plugins": [
            {
                "plugin_type": "FooterPlugin",
                "values": {}
            },
        ],
    },
    "eleicao_navbar": {
        "name": "Navegação",
        "plugins": ["EleicaoNavbarPlugin"],
        "language_fallback": True,
        "default_plugins": [
            {
                "plugin_type": "EleicaoNavbarPlugin",
                "values": {}
            },
        ],
    },
    "eleicao_footer": {
        "name": "Rodapé",
        "plugins": ["EleicaoFooterPlugin"],
        "language_fallback": True,
        "default_plugins": [
            {
                "plugin_type": "EleicaoFooterPlugin",
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
