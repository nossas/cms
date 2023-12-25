from project.settings import *

INSTALLED_APPS += [
    # Build Bootstrap SCSS
    "compressor",
    #
    "nossas",
    "nossas.design",
]

STATICFILES_FINDERS += [
    #
    "compressor.finders.CompressorFinder",
]

COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)

CMS_TEMPLATES += [
    ("nossas/base.html", "NOSSAS"),
]

CMS_PLACEHOLDER_CONF = {
    **CMS_PLACEHOLDER_CONF,
    "main": {
        "name": "Corpo da página",
        "plugins": ["TextPlugin"]
    },
}
