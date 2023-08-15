from typing import Any
from django.core.management.base import BaseCommand
import csv
from django.conf import settings
from eleicao.models import Address


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        csv_filename = settings.BASE_DIR / "eleicao/csv/places.csv"
        choices = []
        with open(csv_filename) as f:
            reader = csv.DictReader(f)
            for row in reader:
                choices.append(
                    Address(
                        state=row["uf"],
                        city=row["city"],
                        neighborhood=row["neighborhood"],
                    )
                )
        Address.objects.bulk_create(choices)

        self.stdout.write("Sucessooo")
