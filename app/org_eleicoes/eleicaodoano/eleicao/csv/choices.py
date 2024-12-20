from django.conf import settings


def get_states(column_label="name"):
    import csv

    csv_filename = settings.BASE_DIR / "org_eleicoes/eleicaodoano/eleicao/csv/states.csv"

    states = []
    with open(csv_filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            states.append((row["subdivision"], row[column_label]))

    return states


def get_ufs():
    return get_states(column_label="subdivision")

# def get_choices(uf, city=None):
#     import csv

#     csv_filename = settings.BASE_DIR / "eleicao/csv/places.csv"
#     choices = []

#     with open(csv_filename) as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             if row["uf"] == uf:
#                 if city:
#                     if city.upper() == row["city"].upper():
#                         choices.append(
#                             (row["neighborhood"].capitalize(), row["neighborhood"].capitalize())
#                         )
#                 else:
#                     choices.append((row["city"].capitalize(), row["city"].capitalize()))

#     return list(set(choices))