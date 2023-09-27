import json
import jwt
import requests

from django import forms
from django.conf import settings

from contrib.bonde.forms import ReferenceBaseModelForm
from tailwind.forms import StyledBaseForm

from .models import PressurePluginModel


class PressurePluginForm(ReferenceBaseModelForm):
    action_kind = "pressure"

    class Meta(ReferenceBaseModelForm.Meta):
        abstract = False
        model = PressurePluginModel


class PressureAjaxForm(StyledBaseForm):
    reference_id = forms.IntegerField(widget=forms.HiddenInput)
    referrer_path = forms.CharField(widget=forms.HiddenInput)

    email_address = forms.EmailField(label="Seu e-mail")
    name = forms.CharField(label="Seu nome", max_length=80)
    phone_number = forms.CharField(label="Seu telefone", max_length=15, required=False)
    email_subject = forms.CharField(label="Assunto", max_length=100)
    email_body = forms.CharField(label="Corpo do e-mail", widget=forms.Textarea)

    class Meta(StyledBaseForm.Meta):
        readonly_fields = ["email_subject", "email_body"]

    def submit(self):
        try:
            activist = {
                "email": self.cleaned_data["email_address"],
                "name": self.cleaned_data["name"],
                "phone": self.cleaned_data["phone_number"],
            }

            input = {
                "email_subject": self.cleaned_data["email_subject"],
                "email_body": self.cleaned_data["email_body"],
                "form_data": json.dumps(self.cleaned_data),
                "token": jwt.encode({}, settings.BONDE_ACTION_SECRET_KEY),
            }

            query = """
                mutation Pressure($activist: ActivistInput!, $input: EmailPressureInput, $widget_id: Int!) {
                create_email_pressure(
                    activist: $activist,
                    widget_id: $widget_id,
                    input: $input
                ) {
                    data
                }
                }
            """
            variables = {
                "activist": activist,
                "input": input,
                "widget_id": self.cleaned_data["reference_id"],
            }

            resp = requests.post(settings.BONDE_ACTION_API_URL, json={"query": query, "variables": variables})
            if resp.status_code == 200:
                print(resp.json())
            else:
                raise Exception("Query failed to run by returning code of {}. {}".format(resp.status_code, query))
        except requests.ConnectionError:
            raise Exception("ConnectionError")
