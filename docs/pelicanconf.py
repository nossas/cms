AUTHOR = "NOSSAS"
SITE_NAME = "Bonde"
SITEURL = ""

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

# Blogroll
# LINKS = (('Pelican', 'https://getpelican.com/'),
#          ('Python.org', 'https://www.python.org/'),
#          ('Jinja2', 'https://palletsprojects.com/p/jinja/'),
#          ('You can modify those links in your config file', '#'),)

MENU_ITEMS = [
    {"title": "Inicio", "url": "/"},
    {
        "title": "Tutorial",
        "url": "/tutoriais/",
        "children": [
            {"title": "Login", "url": "/tutoriais/login/"},
            {"title": "Criar uma página", "url": "/tutoriais/criar-uma-pagina/"},
            # {"title": "Parte 2", "url": ""},
            # {"title": "Parte 3", "url": ""},
        ],
    },
]

# Social widget
SOCIAL = (
    ("You can add links in your config file", "#"),
    ("Another social link", "#"),
)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
