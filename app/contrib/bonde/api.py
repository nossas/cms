# import json
# from datetime import datetime
from django.utils.translation import gettext as _
from contrib.bonde.models import FormEntry, Activist


def create_form_entry(settings: dict, **form_data):
    if not settings.get("widget_id"):
        raise Exception(_("Erro de configuração widget_id"))

    if not settings.get("mobilization_id"):
        raise Exception(_("Erro de configuração mobilization_id"))

    if not settings.get("cached_community_id"):
        raise Exception(_("Erro de configuração cached_community_id"))

    email = form_data.get("email")
    name = form_data.get("name")
  
    # Activist get_or_create 
    activist, created = Activist.objects.get_or_create(email=email)
   
    if created:
        activist.name = name
        activist.save()

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
    fe.widget_id = settings.get("widget_id")
    fe.mobilization_id = settings.get("mobilization_id")
    fe.cached_community_id = settings.get("cached_community_id")

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

    fe.fields = fields
    fe.save()

    return fe