from typing import Any
from django import forms
from colorfield.fields import ColorWidget

from contrib.actions.pressure.models import PressurePluginModel
from .widgets import ActionSelectWidget, ActionChoices


class ReferenceBaseModelForm(forms.ModelForm):
    """ """

    class Meta:
        abstract = True
        fields = ["reference_id"]

    class Media:
        js = ("//ajax.googleapis.com/ajax/libs/jquery/3.7.0/jquery.min.js",)

    # Reference Widget ID
    reference_id = forms.ChoiceField(
        label="Selecione a widget criada no BONDE",
        widget=ActionSelectWidget,
        required=False,
    )

    # Settings Fields
    title = forms.CharField(label="Título do formulário", required=False)
    button_text = forms.CharField(label="Texto do botão", required=False)
    main_color = forms.CharField(
        label="Cor principal", widget=ColorWidget, required=False
    )
    whatsapp_text = forms.CharField(
        label="Texto de compartilhamento por WhatsApp",
        widget=forms.Textarea,
        required=False
    )

    # Settings Widget Kind Form
    action_kind = None

    def __init__(self, *args, **kwargs):
        super(ReferenceBaseModelForm, self).__init__(*args, **kwargs)

        # Configurar tipo de ação para filtrar widgets
        self.fields["reference_id"].choices = ActionChoices(self.action_kind)

        self.prepare_fields()

    def prepare_fields(self):
        if self.instance and self.instance.reference_id:
            obj = self.instance.widget

            self.fields["title"].initial = (
                obj.settings.get("call_to_action")
                or obj.settings.get("title_text")
                or obj.settings.get("title")
            )

            self.fields["button_text"].initial = obj.settings.get("button_text")
            self.fields["main_color"].initial = obj.settings.get("main_color")
            self.fields["whatsapp_text"].initial = obj.settings.get("whatsapp_text")

    def update_widget_settings(self, widget, commit=True):
        widget.settings["call_to_action"] = self.cleaned_data["title"]
        widget.settings["button_text"] = self.cleaned_data["button_text"]
        widget.settings["main_color"] = self.cleaned_data["main_color"]
        widget.settings["whatsapp_text"] = self.cleaned_data["whatsapp_text"]

        if commit:
            widget.save()

        return widget

    def save(self, commit=False) -> Any:
        self.instance = super().save(commit)

        # TODO: Verificar salvar sem necessidade
        self.update_widget_settings(widget=self.instance.widget, commit=True)

        return self.instance
