from django import forms

# from django.contrib import admin

# Register your models here.

from django.utils.translation import ugettext_lazy as _
from djangocms_form_builder import actions

from .api import create_form_entry


@actions.register
class IntegrateWithBonde(actions.FormAction):
    verbose_name = _("Integração com o BONDE")

    class Meta:
        entangled_fields = {
            "action_parameters": ["cached_community_id", "mobilization_id", "widget_id"]
        }

    cached_community_id = forms.IntegerField(label="ID da Comunidade", required=False)
    mobilization_id = forms.IntegerField(label="ID da Mobilização", required=False)
    widget_id = forms.IntegerField(label="ID da Widget", required=False)

    def execute(self, form, request):
        # Integração com o BONDE
        settings = {
            "cached_community_id": self.get_parameter(form, "cached_community_id"),
            "mobilization_id": self.get_parameter(form, "mobilization_id"),
            "widget_id": self.get_parameter(form, "widget_id"),
        }

        if len(list(filter(lambda x: not x, settings.values()))) == 0:
            create_form_entry(settings, **form.cleaned_data)
