# ID da Comunidade: 263
# ID de Mobilização: 7302
# ID da Widget Candidatura: 76494
import json
from datetime import datetime
from contrib.bonde.models import FormEntry, Activist


def create_form_entry(**form_data):
    email = form_data.get("email")
    name = form_data.get("name")
    # Activist get_or_create
    activist = Activist.objects.get(email=email)

    if not activist:
        activist = Activist.objects.create(email=email, name=name)

    state = form_data.get("state")
    city = form_data.get("city")
    activist.first_name = name.split(" ")[0]
    activist.last_name = " ".join(name.split(" ")[1:])
    activist.state = state
    activist.city = city
    activist.save()

    # Montando o FormEntry
    fe = FormEntry()
    fe.activist = activist
    fe.widget_id = 76494
    fe.mobilization_id = 7302
    fe.cached_community_id = 263

    # Fields mapping
    fields = []
    for key, value in form_data.items():
        fields.append(
            {
                "uid": key,
                "kind": "text" if key != "email" else "email",
                "label": key,
                "placeholder": "",
                "required": True,
                "value": value if key != "birth" else value.strftime("%d/%m/%Y"),
            }
        )

    # import ipdb;ipdb.set_trace()
    fe.fields = fields
    fe.save()

    return fe
