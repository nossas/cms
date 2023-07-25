import json

from django import forms
from django.forms import formset_factory

# from contrib.bonde.forms import ReferenceBaseModelForm
from tailwind.forms import StyledBaseForm

from contrib.actions.models import Campaign
from ..models.base import Pressure
from ..models.targets import Target
from ..models.plugins import PressurePluginModel
from .base import PressureAdminForm
from .base import EmailPressureForm, PhonePressureForm, TwitterPressureForm


class SelectOrCreateWidget(forms.Select):
    template_name = "pressure/select_or_create_widget.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["form"] = PressureAdminForm()
        context["formsets"] = self._get_formsets()
        return context

    def _get_formsets(self):
        return [
            formset_factory(EmailPressureForm, extra=1),
            formset_factory(PhonePressureForm, extra=1),
            formset_factory(TwitterPressureForm, extra=1)
        ]


class PressurePluginAddForm(forms.ModelForm):
    action = forms.ModelChoiceField(
        queryset=Pressure.objects,
        # widget=SelectOrCreateWidget,
        blank=True
    )

    class Meta:
        model = PressurePluginModel
        # widgets = {"targets": MultipleTargetSelect}
        fields = "__all__"
    

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     import ipdb;ipdb.set_trace()
    

    # def clean_action(self):
    #     import ipdb;ipdb.set_trace()
    #     action = self.cleaned_data.get("action")
        
    



# class PressurePluginForm(ReferenceBaseModelForm):
#     action_kind = "pressure"

#     class Meta(ReferenceBaseModelForm.Meta):
#         abstract = False
#         model = PressurePluginModel


class PressureAjaxForm(StyledBaseForm):
    action_id = forms.IntegerField(widget=forms.HiddenInput)
    total_actions = forms.CharField(widget=forms.HiddenInput)
    geolocation = forms.JSONField(widget=forms.HiddenInput, required=False)

    email_address = forms.EmailField(label="Seu e-mail")
    name = forms.CharField(label="Seu nome", max_length=80)
    phone_number = forms.CharField(label="Seu telefone", max_length=15, required=False)
    email_subject = forms.CharField(label="Assunto", max_length=100)
    email_body = forms.CharField(label="Corpo do e-mail", widget=forms.Textarea)

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
                "action_id": self.cleaned_data["action_id"],
            },
        )
