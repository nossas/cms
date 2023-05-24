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

    # def add_arguments(self, parser):
    #     parser.add_argument("port", type=int)

    def handle(self, *args, **options):
        # Atualiza site principal para dominio da ferramenta
        site = Site.objects.get(id=1)
        site.domain = "localhost:8000" if settings.DEBUG else "openactiontool.org"
        site.name = "CMS (Open Action Tool)"
        site.save()

        # Cria novos sites
        for domain, name in site_list:
            domain = domain.replace(".org.br", ".localhost:8000") if settings.DEBUG else domain

            Site.objects.get_or_create(name=name, domain=domain)

            self.stdout.write(
                self.style.SUCCESS('"%s" criado com sucesso.' % domain)
            )