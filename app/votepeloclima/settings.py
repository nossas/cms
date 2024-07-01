from pathlib import Path
from project.settings import *


# Root folder to this site config

SITE_DIR = Path(__file__).resolve().parent

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

    "contrib.oauth",
    # "adp.map"
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

ROOT_URLCONF = "votepeloclima.urls"


AUTHENTICATION_BACKENDS = (
    'contrib.oauth.backends.OAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Static files

STATICFILES_FINDERS += [
    #
    "compressor.finders.CompressorFinder",
]

COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)

# DjangoCMS
# Configurações inicials

CMS_TEMPLATES = [
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