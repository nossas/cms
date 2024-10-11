from typing import Any
from django.core.management.base import BaseCommand
import csv
from django.conf import settings
from eleicao.models import PollingPlace


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        csv_filename = settings.BASE_DIR / "eleicao/csv/cts-novo.csv"
        choices = []
        with open(csv_filename) as f:
            reader = csv.DictReader(f)
            for row in reader:
                choices.append(
                    PollingPlace(
                        state=row["state"].strip(),
                        city=row["city"].strip(),
                        place=row["name"].strip(),
                        reference=row["reference"].strip()
                    )
                )
        PollingPlace.objects.bulk_create(choices)

        self.stdout.write(f"Inserido {PollingPlace.objects.count()} CTs com sucesso.")
