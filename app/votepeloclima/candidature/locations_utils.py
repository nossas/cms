from django.conf import settings
from pathlib import Path
import csv
from typing import List

def read_csv_file(file_path: Path) -> List[dict]:
    with open(file_path) as f:
        reader = csv.DictReader(f)
        reader.fieldnames = [field.strip() for field in reader.fieldnames]
        return [row for row in reader]

def get_states(column_label="Nome_UF"):
    csv_filename = Path(settings.BASE_DIR) / "votepeloclima/candidature/csv/places.csv"
    rows = read_csv_file(csv_filename)
    states = set()
    for row in rows:
        uf = row["UF"].strip()
        state_name = row[column_label].strip()
        states.add((uf, state_name))
    return sorted(list(states), key=lambda x: x[1])

def get_ufs():
    return get_states(column_label="Nome_UF")

def get_choices(uf):
    csv_filename = Path(settings.BASE_DIR) / "votepeloclima/candidature/csv/places.csv"
    rows = read_csv_file(csv_filename)
    choices = []
    for row in rows:
        if row["UF"].strip() == uf:
            city_code = row["Código Município Completo"].strip()
            city_name = row["Nome_Município"].strip()
            choices.append((city_code, city_name))
    return sorted(choices, key=lambda x: x[1])
