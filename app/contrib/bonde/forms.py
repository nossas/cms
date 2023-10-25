from typing import Any
from django import forms
from colorfield.fields import ColorWidget

from .widgets import ActionSelectWidget, ActionChoices


class ReferenceBaseModelForm(forms.ModelForm):
    """ """

    class Meta:
        abstract = True
        fields = ["reference_id"]

    class Media:
        js = (
            "//ajax.googleapis.com/ajax/libs/jquery/3.7.0/jquery.min.js",
            "bonde/js/edit-widget-form.js",
        )
        css = {"all": ["bonde/css/edit-widget-form.css"]}

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
    count_text = forms.CharField(label="Contador", required=False)

    whatsapp_text = forms.CharField(
        label="Texto de compartilhamento por WhatsApp",
        widget=forms.Textarea,
        required=False,
    )

    # Post action Fields
    sender_name = forms.CharField(label="Remetente", required=False)
    sender_email = forms.CharField(label="E-mail de resposta", required=False)
    email_subject = forms.CharField(label="Assunto do e-mail", required=False)
    email_text = forms.CharField(
        label="Corpo do e-mail", widget=forms.Textarea, required=False
    )

    # Settings Widget Kind Form
    action_kind = None

    def __init__(self, *args, **kwargs):
        super(ReferenceBaseModelForm, self).__init__(*args, **kwargs)

        # Configurar tipo de ação para filtrar widgets
        self.fields["reference_id"].choices = ActionChoices(self.action_kind)

        if self.instance and self.instance.reference_id:
            self.prepare_fields()

    def prepare_fields(self):
        obj = self.instance.widget

        self.fields["title"].initial = (
            obj.settings.get("call_to_action")
            or obj.settings.get("title_text")
            or obj.settings.get("title")
        )
        self.fields["button_text"].initial = obj.settings.get("button_text")
        self.fields["main_color"].initial = obj.settings.get("main_color")
        self.fields["count_text"].initial = obj.settings.get("count_text")

        self.fields["whatsapp_text"].initial = obj.settings.get("whatsapp_text")

        self.fields["sender_name"].initial = obj.settings.get("sender_name")
        self.fields["sender_email"].initial = obj.settings.get("sender_email")
        self.fields["email_subject"].initial = obj.settings.get("email_subject")
        self.fields["email_text"].initial = obj.settings.get("email_text")

    def update_widget_settings(self, widget, commit=True):
        widget.settings["call_to_action"] = self.cleaned_data["title"]
        widget.settings["button_text"] = self.cleaned_data["button_text"]
        widget.settings["main_color"] = self.cleaned_data["main_color"]
        widget.settings["count_text"] = self.cleaned_data["count_text"]

        widget.settings["whatsapp_text"] = self.cleaned_data["whatsapp_text"]

        widget.settings["sender_name"] = self.cleaned_data["sender_name"]
        widget.settings["sender_email"] = self.cleaned_data["sender_email"]
        widget.settings["email_subject"] = self.cleaned_data["email_subject"]
        widget.settings["email_text"] = self.cleaned_data["email_text"]

        if commit:
            widget.save()

        return widget

    def save(self, commit=False) -> Any:
        self.instance = super().save(commit)

        # TODO: Verificar salvar sem necessidade
        self.update_widget_settings(widget=self.instance.widget, commit=True)

        return self.instance
