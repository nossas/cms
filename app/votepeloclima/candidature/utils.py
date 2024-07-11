from django.conf import settings
import csv

def get_states(column_label="Nome_UF"):
    csv_filename = settings.BASE_DIR / "votepeloclima/candidature/csv/places.csv"
    states = set()
    with open(csv_filename) as f:
        reader = csv.DictReader(f)
        reader.fieldnames = [field.strip() for field in reader.fieldnames]
        for row in reader:
            uf = row["UF"].strip()
            state_name = row[column_label].strip()
            states.add((uf, state_name))
    return sorted(list(states), key=lambda x: x[1])

def get_ufs():
    return get_states(column_label="Nome_UF")

def get_choices(uf):
    csv_filename = settings.BASE_DIR / "votepeloclima/candidature/csv/places.csv"
    choices = set()
    with open(csv_filename) as f:
        reader = csv.DictReader(f)
        reader.fieldnames = [field.strip() for field in reader.fieldnames]
        for row in reader:
            if row["UF"].strip() == uf:
                city_code = row["Código Município Completo"].strip()
                city_name = row["Nome_Município"].strip()
                choices.append((city_code, city_name))
    return sorted(list(choices), key=lambda x: x[1])
