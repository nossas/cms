from project.settings import *
from pathlib import Path

SITE_DIR = Path(__file__).resolve().parent

DEFAULT_DB_SQLITE = BASE_DIR / "eleicao.sqlite3"

DATABASES.update(
    {
        "default": env.db_url("CMS_DATABASE_URL", f"sqlite:///{DEFAULT_DB_SQLITE}"),
    }
)

INSTALLED_APPS += [
    "org_eleicoes.eleicaodoano.eleicao",
]

MIDDLEWARE += [
    "org_eleicoes.eleicaodoano.eleicao.middleware.EleicaoRedirectMiddleware",
]

ROOT_URLCONF = "org_eleicoes.eleicaodoano.urls"

CMS_TEMPLATES += [
    ("frontend/landpage/page.html", "Landpage"),
    ("eleicao/eleicao_template.html", "A Eleição do Ano"),
]