from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site

site_list = (
    # Dominios de grupos de trabalho
    ('nossas.org.br', 'NOSSAS'),
    ('meurio.org.br', 'Meu Rio'),
    ('minhamanaus.org.br', 'Minha Manaus'),
)

class Command(BaseCommand):
    help = "Criar sites utilizados nessa aplicação"

    def add_arguments(self, parser):
        parser.add_argument("domain", type=str)

    def handle(self, *args, **options):
        # Atualiza site principal para dominio da ferramenta
        domain = options.get("domain")
        site = Site.objects.get(id=1)
        site.domain = domain
        site.name = "Site CMS"
        site.save()