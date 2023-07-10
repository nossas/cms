import os

AUTHOR = "NOSSAS"

SITE_NAME = "BondeCMS - Documentação"

SITEURL = os.getenv("PELICAN_SITEURL", "")

PATH = "content"

THEME = "pelican/themes/pelican-docs"

TIMEZONE = "America/Sao_Paulo"

DEFAULT_LANG = "pt"

PLUGIN_PATHS = ["pelican/plugins"]

PLUGINS = ["page_hierarchy"]

# https://github.com/akhayyat/pelican-page-hierarchy
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'
SLUGIFY_SOURCE = 'basename'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

MENU_ITEMS = [
    {"title": "Inicio", "url": f"{SITEURL}/"},
    {
        "title": "Tutorial",
        "url": f"{SITEURL}/tutoriais/",
        "children": [
            {"title": "Login", "url": f"{SITEURL}/tutoriais/login/"},
            {"title": "Criar página", "url": f"{SITEURL}/tutoriais/criar-pagina/"},
            {"title": "Editar página", "url": f"{SITEURL}/tutoriais/editar-pagina/"},
            {"title": "Salvar e publicar página", "url": f"{SITEURL}/tutoriais/salvar-e-publicar-pagina/"},
            {"title": "Configurar o GA", "url": f"{SITEURL}/tutoriais/google-analytics/"},
        ],
    },
]