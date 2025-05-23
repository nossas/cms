"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import environ
from pathlib import Path


env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, "django-insecure-secret-key"),
    ALLOWED_HOSTS=(list, None),
    DISABLE_RECAPTCHA=(bool, False),
    RECAPTCHA_PUBLIC_KEY=(str, "MyRecaptchaKey123"),
    RECAPTCHA_PRIVATE_KEY=(str, "MyRecaptchaPrivateKey456"),
    AWS_ACCESS_KEY_ID=(str, ""),
    AWS_SECRET_ACCESS_KEY=(str, ""),
    AWS_REGION=(str, ""),
    ETCD_HOST=(str, "127.0.0.1"),
    ETCD_PORT=(int, 2379),
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

environ.Env.read_env(BASE_DIR / ".env")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

X_FRAME_OPTIONS = "SAMEORIGIN"

# Application definition

INSTALLED_APPS = [
    "admin_styled",
    "tailwind",
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
    "captcha",
    "colorfield",
    "django_select2",
    "django_jsonform",
    "djangocms_form_builder",
    # My Apps
    "contrib.actions.pressure",
    "contrib.bonde",
    "contrib.campaign",
    "contrib.frontend",
    "contrib.frontend.landpage",
    "contrib.frontend.grid",
    "contrib.frontend.maps",
    "contrib.ga",
    "contrib.partners",
    #
    # "contrib.domains.route53",
    # "contrib.domains.traefik",
    # Experimentação
    "django_social_share",
    #
    # "django_prometheus"

    'project',
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
    #
    # "django_prometheus.middleware.PrometheusAfterMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "project.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DEFAULT_DB_SQLITE = BASE_DIR / "db.sqlite3"

DATABASES = {
    "default": env.db_url("CMS_DATABASE_URL", f"sqlite:///{DEFAULT_DB_SQLITE}"),
    # Add tmp sqlite file to build image
    "bonde": env.db_url("BONDE_DATABASE_URL", "sqlite:////tmp/bonde.sqlite3"),
}

DATABASE_ROUTERS = [
    "contrib.bonde.router.AuthRouter",
]

BONDE_ACTION_API_URL = env.str(
    "BONDE_ACTION_API_URL", "http://api-graphql.localhost/v1/graphql"
)

BONDE_ACTION_SECRET_KEY = env.str("BONDE_ACTION_SECRET_KEY", "")

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    # 'django.contrib.auth.backends.ModelBackend',
    "contrib.bonde.backends.BondeSiteBackend",
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "pt-br"

LANGUAGES = [
    ("pt-br", "Português"),
]

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles/"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# only required for local file storage and serving, in development
MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media/"


# Thumbnails
# https://easy-thumbnails.readthedocs.io/en/latest/

THUMBNAIL_PROCESSORS = (
    "easy_thumbnails.processors.colorspace",
    "easy_thumbnails.processors.autocrop",
    # 'easy_thumbnails.processors.scale_and_crop',
    "filer.thumbnail_processors.scale_and_crop_with_subject_location",
    "easy_thumbnails.processors.filters",
)

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Sites
# https://docs.djangoproject.com/en/4.2/ref/contrib/sites/

SITE_ID = 1

# reCaptcha
DISABLE_RECAPTCHA = env("DISABLE_RECAPTCHA")

RECAPTCHA_PUBLIC_KEY = env("RECAPTCHA_PUBLIC_KEY")

RECAPTCHA_PRIVATE_KEY = env("RECAPTCHA_PRIVATE_KEY")

SILENCED_SYSTEM_CHECKS = ["captcha.recaptcha_test_key_error"]


# Bonde Router

# AWS
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")

AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")

AWS_REGION = env("AWS_REGION")

# Etcd
ETCD_HOST = env("ETCD_HOST")

ETCD_PORT = env("ETCD_PORT")
