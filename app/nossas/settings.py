from project.settings import *

# Apps

INSTALLED_APPS += [
    # Build Bootstrap SCSS
    "compressor",
    #
    "nossas",
    "nossas.design",
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


# CMS

CMS_TEMPLATES += [
    ("nossas/base.html", "NOSSAS"),
]

CMS_PLACEHOLDER_CONF = {
    **CMS_PLACEHOLDER_CONF,
    "main": {"name": "Corpo da página", "plugins": ["TextPlugin"]},
}
