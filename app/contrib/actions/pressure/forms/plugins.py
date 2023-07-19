import json

from django import forms

from contrib.bonde.forms import ReferenceBaseModelForm
from tailwind.forms import StyledBaseForm

from ..models import PressurePluginModel


class PressurePluginForm(ReferenceBaseModelForm):
    action_kind = "pressure"

    class Meta(ReferenceBaseModelForm.Meta):
        abstract = False
        model = PressurePluginModel


class PressureAjaxForm(StyledBaseForm):
    reference_id = forms.IntegerField(widget=forms.HiddenInput)

    email_address = forms.EmailField(label="Seu e-mail")
    name = forms.CharField(label="Seu nome", max_length=80)
    phone_number = forms.CharField(label="Seu telefone", max_length=15, required=False)
    email_subject = forms.CharField(label="Assunto", max_length=100)
    email_body = forms.CharField(label="Corpo do e-mail", widget=forms.Textarea)
    city = forms.CharField(widget=forms.HiddenInput)

    class Meta(StyledBaseForm.Meta):
        readonly_fields = ["email_subject", "email_body"]

    def submit(self):
        activist = {
            "email": self.cleaned_data["email_address"],
            "name": self.cleaned_data["name"],
            "phone": self.cleaned_data["phone_number"],
        }

        input = {
            "email_subject": self.cleaned_data["email_subject"],
            "email_body": self.cleaned_data["email_body"],
            "form_data": json.dumps(self.cleaned_data),
        }

        print(
            "Submitting ->>",
            {
                "activist": activist,
                "input": input,
                "widget_id": self.cleaned_data["reference_id"],
            },
        )
