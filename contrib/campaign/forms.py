from typing import Any, Dict
from django import forms
from django.db import transaction

# from cms.forms.wizards import CreateCMSPageForm
from djangocms_text_ckeditor.widgets import TextEditorWidget

from tailwind.widgets import RadioSelect, CheckboxSelectMultiple
from tailwind.fields import InputArrayField

from contrib.bonde.widgets import BondeWidget

from .models import Pressure, SharingChoices


class PressureForm(forms.Form):
    # People Fields
    email_address = forms.EmailField(
        label="Seu e-mail",
        widget=forms.EmailInput(attrs={"placeholder": " "}),
    )

    name = forms.CharField(
        label="Seu nome",
        max_length=80,
        widget=forms.TextInput(attrs={"placeholder": " "}),
    )

    phone_number = forms.CharField(
        label="Seu telefone",
        required=False,
        max_length=15,
        widget=forms.TextInput(attrs={"placeholder": " "}),
    )

    # Action Fields
    email_subject = forms.CharField(label="Assunto", max_length=100, disabled=True, widget=forms.TextInput(attrs={"placeholder": " "}),)

    email_body = forms.CharField(
        label="Corpo do e-mail", disabled=True, widget=forms.Textarea(attrs={"placeholder": " "})
    )

    def __init__(self, *args, **kwargs):
        super(PressureForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs[
                "class"
            ] = "block input input-bordered px-2.5 pb-2.5 pt-8 w-full text-sm focus:outline-none focus:ring-0 peer"

            if isinstance(visible.field.widget, forms.Textarea):
                visible.field.widget.attrs["class"] += " h-28"


class PressureSettingsForm(forms.ModelForm):
    widget = forms.IntegerField(widget=forms.Select)

    email_subject = InputArrayField(
        label="Assunto do e-mail para os alvos",
        num_widgets=10
    )

    disable_editing = forms.ChoiceField(
        label="Desabilitar edição do e-mail e do assunto pelos ativistas?",
        choices=(
            (True, "Desabilitar"),
            (False, "Habilitar")
        ),
        widget=RadioSelect,
        initial=True
    )

    sharing = forms.MultipleChoiceField(
        label="Opções de compartilhamento",
        choices=SharingChoices.choices,
        widget=CheckboxSelectMultiple
    )

    class Meta:
        model = Pressure
        fields = "__all__"

    def clean(self):
        cleaned_data = super(PressureSettingsForm, self).clean()
        # import ipdb;ipdb.set_trace()
        return cleaned_data

    def save(self, commit):
        # import ipdb;ipdb.set_trace()
        return super(PressureSettingsForm, self).save(commit)