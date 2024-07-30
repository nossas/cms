from pathlib import Path
from django.urls import reverse_lazy
from project.settings import *


# Root folder to this site
SITE_DIR = Path(__file__).resolve().parent.parent

# Databases

DEFAULT_DB_SQLITE = BASE_DIR / "votepeloclima.sqlite3"

DATABASES.update(
    {
        "default": env.db_url("CMS_DATABASE_URL", f"sqlite:///{DEFAULT_DB_SQLITE}"),
    }
)


# Installed apps

INSTALLED_APPS = [
    # "admin_styled",
    # "tailwind",
    # Override third apps templates
    "contrib.ds.admin_style",
    "djangocms_admin_style",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    # http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    #
    "adminsortable2",
    # Django CMS
    "cms",
    "menus",
    "treebeard",
    "sekizai",
    # Django Filer - optional, but used in most projects
    "filer",
    "easy_thumbnails",
    # some content plugins - optional, but used in most projects
    "djangocms_picture",
    "djangocms_text_ckeditor",
    "djangocms_video",
    "djangocms_snippet",
    # Third apps
    "colorfield",
    "compressor",
    "captcha",
    "django_select2",
    "django_jsonform",
    "djangocms_form_builder",
    "formtools",
    "crispy_forms",
    "crispy_bootstrap5",
    "bootstrap_datepicker_plus",
    # My Apps
    "contrib.bonde",
    "contrib.ga",

    "contrib.ds",
    "contrib.ds.accordion",
    "contrib.ds.blocks",
    "contrib.ds.card",
    "contrib.ds.carousel",
    "contrib.ds.counter",
    "contrib.ds.grid",
    "contrib.ds.link",
    "contrib.ds.picture",
    "contrib.ds.tooltip",
    # Project Apps
    "contrib.oauth",
    "org_eleicoes.votepeloclima.candidature",
]

MIDDLEWARE = [
    # "django_prometheus.middleware.PrometheusBeforeMiddleware",
    #
    "django.middleware.security.SecurityMiddleware",
    "project.middleware.WwwRedirectMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
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
    "contrib.oauth.middleware.NoDjangoAdminForEndUserMiddleware",
    #
    # "django_prometheus.middleware.PrometheusAfterMiddleware",
]

# URLs

ROOT_URLCONF = "org_eleicoes.votepeloclima.urls"


AUTHENTICATION_BACKENDS = [
    'contrib.oauth.backends.OAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
 ] + AUTHENTICATION_BACKENDS

# Static files

STATICFILES_FINDERS += [
    #
    "compressor.finders.CompressorFinder",
]

COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [SITE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "sekizai.context_processors.sekizai",
                "contrib.ga.context_processors.ga",
                "django.template.context_processors.request",
            ],
        },
    },
]

# DjangoCMS
# Configurações inicials

CMS_TEMPLATES = [
    ("votepeloclima/base.html", "Vote pelo Clima"),
    ("ds/base.html", "[DS] Padrão"),
    ("ds/base_navbar_footer.html", "[DS] Navbar + Footer"),
    # ("ga/base.html", "Base Google Analytics"),
]

CMS_PLACEHOLDER_CONF = {}

DJANGOCMS_PICTURE_RESPONSIVE_IMAGES = True

# DjangoCMS Form Builder Submodule

DJANGOCMS_FORMS_REQUIRED_CSS_CLASS = "required"

DJANGOCMS_FORMS_FORM_PLUGIN_CHILD_CLASSES = [
    "BlockPlugin",
    "ButtonPlugin",
]

# CKEDITOR_SETTINGS = {
#     **CKEDITOR_SETTINGS,
#     "colorButton_colors": "0F5427,20A54B,D8952A,F0A42B,C32C18,EA4F83,1D3D90,080808,222222,555555,F5F4F0,FFFFFF",
# }


EMAIL_HOST = env("SMTP_HOST", default="localhost")

EMAIL_PORT = env("SMTP_PORT", default=1025)

EMAIL_HOST_USER = env("SMTP_USER", default="")

EMAIL_HOST_PASSWORD = env("SMTP_PASS", default="")

EMAIL_USE_TLS = env("SMTP_USE_TLS", default=False)

EMAIL_USE_SSL = env("SMTP_USE_SSL", default=False)

# Django Crispy Forms

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

# Oauth App
OAUTH_REDIRECT_LOGIN_URL = reverse_lazy("dashboard")