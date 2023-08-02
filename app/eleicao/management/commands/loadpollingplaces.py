from typing import Any, Optional
from django.core.management.base import BaseCommand
import csv
from django.conf import settings
from eleicao.models import Address, PollingPlace


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        csv_filename = settings.BASE_DIR / "eleicao/csv/abrangencia-rj.csv"
        # choices = []
        with open(csv_filename) as f:
            reader = csv.DictReader(f)
            for row in reader:
                ct_name = row["ct_name"]
                # print(f"CT: {ct_name}")
                abrangencia = list(map(
                    lambda x: x.upper(),
                    row["abrangencia"].split(";")
                ))
                # print(f"Abrangencia: {len(abrangencia)}")
                city = row["city"]
                state = row["state"]

                qs = Address.objects.filter(state=state, city=city.upper()).filter(
                    neighborhood__in=abrangencia
                )

                polling_place = PollingPlace.objects.create(name=ct_name)
                polling_place.places.set(qs)
                polling_place.save()
                # print(f"Abrangencia filtrado: {len(qs)}")

        # Address.objects.bulk_create(choices)

        self.stdout.write("Sucessooo")
