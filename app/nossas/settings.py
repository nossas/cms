from project.settings import *

# Apps

INSTALLED_APPS += [
    # Build Bootstrap SCSS
    "compressor",
    #
    "djangocms_frontend",
    "djangocms_frontend.contrib.utilities",
    "djangocms_frontend.contrib.link",
    #
    "nossas",
    "nossas.design",
    "nossas.plugins",
    "nossas.apps.campaigns",
    "nossas.apps.team",
]


# Static files

STATICFILES_FINDERS += [
    #
    "compressor.finders.CompressorFinder",
]

COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)


# Middlewares

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "project.middleware.WwwRedirectMiddleware",
    "eleicao.middleware.EleicaoRedirectMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # Add i18n middleware
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "contrib.bonde.middleware.SiteMiddleware",
    "cms.middleware.user.CurrentUserMiddleware",
    "cms.middleware.page.CurrentPageMiddleware",
    "cms.middleware.toolbar.ToolbarMiddleware",
    "cms.middleware.language.LanguageCookieMiddleware",
]

# Internationalization

USE_I18N = True

LANGUAGES = [
    ("pt-br", "Português"),
    ("en", "Inglês"),
]


# URLs

ROOT_URLCONF = "nossas.urls"


# CMS

CMS_TEMPLATES = [
    ("nossas/base.html", "NOSSAS"),
] + CMS_TEMPLATES

CMS_PLACEHOLDER_CONF = {
    **CMS_PLACEHOLDER_CONF,
    "nossas_main": {
        "name": "Corpo da página",
        "plugins": [
            "TextPlugin",
            "BoxPlugin",
            "SliderPlugin",
            "TeamAccordionPlugin",
            "FilterCampaignListPlugin",
        ],
    },
    "nossas_navbar": {
        "name": "Navegação",
        "plugins": ["NossasNavbarPlugin"],
        "default_plugins": [{"plugin_type": "NossasNavbarPlugin", "values": {}}],
    },
    "nossas_footer": {
        "name": "Rodapé",
        "plugins": ["SiteFooterPlugin"],
        "default_plugins": [{"plugin_type": "SiteFooterPlugin", "values": {}}],
    },
}

# DjangoCMS Picture

DJANGOCMS_PICTURE_TEMPLATES = [
    ("full_width", "Full width"),
]

# Design

DESIGN_THEME_COLORS = [
    ("Azul NOSSAS", "rgb(35,61,144)", "233D90"),
    ("Verde claro NOSSAS", "rgb(145,206,193)", "91CEC1"),
    ("Bege NOSSAS", "rgb(247,247,237)", "F7F7ED"),
    ("Vermelho NOSSAS", "rgb(224,36,55)", "E02437"),
    ("Amarelo NOSSAS", "rgb(248,173,57)", "F8AD39"),
    ("Rosa NOSSAS", "rgb(246,183,193)", "F6B7C1"),
    ("Verde NOSSAS", "rgb(140,173,106)", "8CAD6A"),
    ("Laranja NOSSAS", "rgb(235,94,59)", "EB5E3B"),
    ("Cinza extra NOSSAS", "rgb(67,57,57)", "433939"),
]

# CKEditor
CKEDITOR_EXTRA_PLUGINS = [
    *CKEDITOR_SETTINGS.get("extraPlugins", "").split(","),
    "colorbutton",
]

CKEDITOR_SETTINGS = {
    **CKEDITOR_SETTINGS,
    "extraPlugins": ",".join(CKEDITOR_EXTRA_PLUGINS),
    "colorButton_colors": ",".join([args[-1] for args in DESIGN_THEME_COLORS]),
    "toolbar_CMS": [*CKEDITOR_SETTINGS.get("toolbar_CMS", []), "/", ["cmsplugins"]],
}
