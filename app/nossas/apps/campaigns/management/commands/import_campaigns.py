import itertools
from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.db.models import Q, Prefetch
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

from contrib.bonde.models import Community, Mobilization
from nossas.apps.campaigns.utils import import_mobilization

# from polls.models import Question as Poll


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--period", type=str)

    def handle(self, *args, **options):
        q = Q()
        for name in [
            "Mobilizações NOSSAS",
            "Rede nossas cidades",
            "Beta",
            "Ninguém fica pra trás",
            "Minha Sampa",
            "Minha Manaus",
            "Minha BH",
            "Meu Rio",
            "Amazônia de pé",
        ]:
            q |= Q(name__icontains=name)

        filters = {"status": "active"}

        if options["period"]:
            year_start, year_end = options["period"].split(",")
            filters.update(
                {
                    "created_at__year__gte": int(year_start),
                    "created_at__year__lte": int(year_end),
                }
            )

        qs = Community.objects.filter(q).prefetch_related(
            Prefetch(
                "mobilization_set",
                queryset=Mobilization.objects.filter(**filters),
            )
        )

        mobilizations = list(
            itertools.chain.from_iterable(map(lambda x: x.mobilization_set.all(), qs))
        )

        site = Site.objects.get(name="NOSSAS")
        user = User.objects.get(username="igor@nossas.org")

        for m in mobilizations:
            try:
                import_mobilization(m.id, site, user)
            except Exception as err:
                import ipdb;ipdb.set_trace()
                self.stdout.write(
                    self.style.ERROR(
                        f"Falha ao tentar importar a Mobilização[{m.id}]: {m.name}."
                    )
                )
