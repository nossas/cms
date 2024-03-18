from pathlib import Path
from project.settings import *

# Root folder to this site config
SITE_DIR = Path(__file__).resolve().parent

# Databases
DEFAULT_DB_SQLITE = BASE_DIR / "nossas.sqlite3"

DATABASES.update(
    {
        "default": env.db_url("CMS_DATABASE_URL", f"sqlite:///{DEFAULT_DB_SQLITE}"),
    }
)

# Apps
# Used to override plugins template
INSTALLED_APPS = (
    [
        "nossas.design",
    ]
    + INSTALLED_APPS
    + [
        "django_jsonform",
        "tag_fields",
        # Build Bootstrap SCSS
        "compressor",
        #
        "nossas",
        "nossas.apps",
        "nossas.plugins",
        # Override HTMLs
        "djangocms_frontend",
        "djangocms_frontend.contrib.utilities",
        "djangocms_frontend.contrib.link",
    ]
)


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

LOCALE_PATHS = (
    SITE_DIR / 'locale',
)

# URLs

ROOT_URLCONF = "nossas.urls"


# CMS

NOSSAS_CONTENT_PLUGINS = [
    "AccordionPlugin",
    "BootstrapGridPlugin",
    "BreadcrumbPlugin",
    "BreaklinePlugin",
    "CampaignListPlugin",
    "CardPlugin",
    "ContainerPlugin",
    "FormPlugin",
    "GalleryPlugin",
    "HeaderPlugin",
    "HeadlinePlugin",
    "PdfViewerPlugin",
    "PicturePlugin",
    "SliderJobsPlugin",
    "SliderPlugin",
    "SocialSharePlugin",
    "TeamAccordionPlugin",
    "TextPlugin",
    "VideoPlayerPlugin",
]

CMS_TEMPLATES = [
    ("nossas/page.html", "NOSSAS Página"),
    ("nossas/home.html", "NOSSAS Home Full Page"),
] + CMS_TEMPLATES

CMS_PLACEHOLDER_CONF = {
    **CMS_PLACEHOLDER_CONF,
    "nossas_page_content": {
        "name": "Corpo da página",
        "plugins": NOSSAS_CONTENT_PLUGINS
        + ["BoxPlugin", "HeaderImagePlugin", "OurCitiesProjectPlugin"],
    },
    "nossas_page_navbar": {
        "name": "Navegação",
        "plugins": ["NossasNavbarPlugin"],
        "default_plugins": [{"plugin_type": "NossasNavbarPlugin", "values": {}}],
    },
    "nossas_page_footer": {
        "name": "Rodapé",
        "plugins": ["SiteFooterPlugin"],
        "default_plugins": [{"plugin_type": "SiteFooterPlugin", "values": {}}],
    },
    "nossas_home_content": {
        "name": "Slides",
        "plugins": [
            "FullPageSliderContentPlugin",
        ],
    },
    # Modelos
    "campaign_placeholder": {
        "name": "Conteúdo da Página",
        "plugins": [
            "TextPlugin",
            "GalleryPlugin",
            "ContainerPlugin",
            "SliderPlugin",
            "ContainerPlugin",
            "NavigateCampaignsPlugin",
        ],
    },
}

# DjangoCMS Picture

DJANGOCMS_PICTURE_TEMPLATES = [
    ("full_width", "Full width"),
    ("background", "Background"),
]

# Design

DESIGN_THEME_COLORS = [
    ("Verde claro NOSSAS", "rgb(145,206,193)", "91CEC1"),
    ("Bege NOSSAS", "rgb(247,247,237)", "F7F7ED"),
    ("Vermelho NOSSAS", "rgb(224,36,55)", "E02437"),
    ("Amarelo NOSSAS", "rgb(248,173,57)", "F8AD39"),
    ("Rosa NOSSAS", "rgb(246,183,193)", "F6B7C1"),
    ("Verde NOSSAS", "rgb(140,173,106)", "8CAD6A"),
    ("Laranja NOSSAS", "rgb(235,94,59)", "EB5E3B"),
    ("Cinza extra NOSSAS", "rgb(67,57,57)", "433939"),
    ("Preto NOSSAS", "rgb(29,29,27)", "1D1D1B"),
    ("Branco NOSSAS", "rgb(255,255,255)", "FFFFFF"),
    # Obrigatoriamente precisa ser o ultimo da lista para sobrescrever outras cores
    ("Azul NOSSAS", "rgb(35,61,144)", "233D90"),
]

DESIGN_THEME_TEXT_COLORS = [
    ("Verde claro NOSSAS", "rgb(29,29,27)"),
    ("Bege NOSSAS", "rgb(29,29,27)"),
    ("Vermelho NOSSAS", "rgb(246,183,193)"),
    ("Amarelo NOSSAS", "rgb(67,57,57)"),
    ("Rosa NOSSAS", "rgb(67,57,57)"),
    ("Verde NOSSAS", "rgb(255,255,255)"),
    ("Laranja NOSSAS", "rgb(255,255,255)"),
    ("Cinza extra NOSSAS", "rgb(247,247,237)"),
    ("Preto NOSSAS", "rgb(255,255,255)"),
    ("Branco NOSSAS", "rgb(29,29,27)"),
    # Obrigatoriamente precisa ser o ultimo da lista para sobrescrever outras cores
    ("Azul NOSSAS", "rgb(247,247,237)"),
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

CKEDITOR_SETTINGS_JOB_MODEL = {
    "toolbar_HTMLField": [
        ["Undo", "Redo"],
        ["Format", "Styles"],
        [
            "Bold",
            "Italic",
            "Underline",
            "-",
            "Subscript",
            "Superscript",
            "-",
            "RemoveFormat",
        ],
        ["NumberedList", "BulletedList"],
    ]
}
