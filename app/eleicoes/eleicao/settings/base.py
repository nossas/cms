from project.settings.base import *
from pathlib import Path

SITE_DIR = Path(__file__).resolve().parent

DEFAULT_DB_SQLITE = BASE_DIR / "eleicao.sqlite3"

DATABASES.update(
    {
        "default": env.db_url("CMS_DATABASE_URL", f"sqlite:///{DEFAULT_DB_SQLITE}"),
    }
)

INSTALLED_APPS += [
    "eleicoes.eleicao",
]

MIDDLEWARE += [
    "eleicoes.eleicao.middleware.EleicaoRedirectMiddleware",
]

ROOT_URLCONF = "eleicoes.eleicao.urls"

STATICFILES_FINDERS += [
    "compressor.finders.CompressorFinder",
]

COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)

# DjangoCMS
CMS_TEMPLATES = [
    ("ds/base.html", "[DS] Padrão"),
    ("ds/base_navbar_footer.html", "[DS] Navbar + Footer"),
]

CMS_PLACEHOLDER_CONF = {}

DJANGOCMS_PICTURE_RESPONSIVE_IMAGES = True

# DjangoCMS Form Builder Submodule
DJANGOCMS_FORMS_REQUIRED_CSS_CLASS = "required"
DJANGOCMS_FORMS_FORM_PLUGIN_CHILD_CLASSES = [
    "BlockPlugin",
    "ButtonPlugin",
]
