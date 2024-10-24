import os
from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.management import CommandError

class Command(BaseCommand):
    help = 'Cria um novo app/site em um grupo específico'

    def add_arguments(self, parser):
        parser.add_argument('group', type=str, help='Nome do grupo onde o app será criado')
        parser.add_argument('app_name', type=str, help='Nome do novo app/site')

    def handle(self, *args, **kwargs):
        group = kwargs['group']
        app_name = kwargs['app_name']

        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        group_dir = base_dir / group
        app_dir = group_dir / app_name
        settings_dir = app_dir / 'settings'
        urls_file = app_dir / 'urls.py'

        try:
            # Verifica se o grupo já existe
            if not group_dir.exists():
                self.stdout.write(self.style.WARNING(f'O grupo {group} não existe. Deseja criar? [S/N]'))
                choice = input().lower()
                if choice != 's':
                    raise CommandError(f'Criação cancelada. O grupo {group} não existe.')

                # Cria o diretório do grupo
                os.makedirs(group_dir)

                # Cria o arquivo __init__.py no diretório do grupo
                with open(group_dir / '__init__.py', 'w') as f:
                    f.write('')

            # Cria as pastas necessárias
            os.makedirs(settings_dir)

            # Cria os arquivos __init__.py
            with open(app_dir / '__init__.py', 'w') as f:
                f.write('')
            with open(settings_dir / '__init__.py', 'w') as f:
                f.write('from .base import *\n')

            # Cria o arquivo base.py dentro de settings
            with open(settings_dir / 'base.py', 'w') as f:
                f.write(self.get_base_settings_content(group, app_name))

            # Cria o arquivo urls.py
            with open(urls_file, 'w') as f:
                f.write(self.get_urls_content())

            self.stdout.write(self.style.SUCCESS(f'App/site {app_name} criado com sucesso em {group_dir}'))

        except FileExistsError:
            raise CommandError(f'O diretório {settings_dir} já existe.')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao criar o app/site: {str(e)}'))

    def get_base_settings_content(self, group, app_name):
        return f"""
from project.settings.base import *
from pathlib import Path

SITE_DIR = Path(__file__).resolve().parent

DEFAULT_DB_SQLITE = BASE_DIR / "{app_name}.sqlite3"

DATABASES.update(
    {{
        "default": env.db_url("CMS_DATABASE_URL", f"sqlite:///{{DEFAULT_DB_SQLITE}}"),
    }}
)

INSTALLED_APPS += [
    "{group}.{app_name}",
]

ROOT_URLCONF = "{group}.{app_name}.urls"

STATICFILES_FINDERS += [
    "compressor.finders.CompressorFinder",
]

COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)

# DjangoCMS
CMS_TEMPLATES = [
    ("ds/base.html", "[DS] Padrão"),
    ("ds/base_navbar_footer.html", "[DS] Navbar + Footer"),
]

CMS_PLACEHOLDER_CONF = {{}}

DJANGOCMS_PICTURE_RESPONSIVE_IMAGES = True

# DjangoCMS Form Builder Submodule
DJANGOCMS_FORMS_REQUIRED_CSS_CLASS = "required"
DJANGOCMS_FORMS_FORM_PLUGIN_CHILD_CLASSES = [
    "BlockPlugin",
    "ButtonPlugin",
]
"""

    def get_urls_content(self):
        return """
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include


urlpatterns = [
    # path("monitoring/", include("django_prometheus.urls")),
    path("admin/", admin.site.urls),
    path("select2/", include("django_select2.urls")),
    path("", include("cms.urls")),
]

urlpatterns += staticfiles_urlpatterns()

handler404 = "contrib.frontend.views.error_404"
handler500 = "contrib.frontend.views.error_500"

if settings.DEBUG:
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
"""