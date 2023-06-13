import json

from django import forms

from tailwind.widgets import RadioSelect, CheckboxSelectMultiple
from tailwind.fields import InputArrayField

from contrib.bonde.models import Widget as BondeWidget

from .models import Pressure, SharingChoices


class PressureForm(forms.Form):
    instance = forms.IntegerField(widget=forms.HiddenInput)
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
    email_subject = forms.CharField(
        label="Assunto",
        max_length=100,
        disabled=True,
        widget=forms.TextInput(attrs={"placeholder": " "}),
    )

    email_body = forms.CharField(
        label="Corpo do e-mail",
        disabled=True,
        widget=forms.Textarea(attrs={"placeholder": " "}),
    )

    def __init__(self, *args, **kwargs):
        super(PressureForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs[
                "class"
            ] = "block input input-bordered px-2.5 pb-2.5 pt-8 w-full text-sm focus:outline-none focus:ring-0 peer"

            if isinstance(visible.field.widget, forms.Textarea):
                visible.field.widget.attrs["class"] += " h-28"

    def submit(self):
        instance = Pressure.objects.get(id=self.cleaned_data["instance"])
        payload = dict()

        payload["activist"] = dict(
            email=self.cleaned_data["email_address"],
            name=self.cleaned_data["name"],
            phone=self.cleaned_data["phone_number"],
        )

        payload["widget_id"] = instance.widget

        payload["input"] = dict(
            email_subject=self.cleaned_data["email_subject"],
            email_body=self.cleaned_data["email_body"],
            form_data=json.dumps(self.cleaned_data),
        )

        print("Submitting ->>", payload)


class PressureSettingsForm(forms.ModelForm):
    widget = forms.IntegerField(widget=forms.Select)

    email_subject = InputArrayField(
        label="Assunto do e-mail para os alvos", num_widgets=10
    )

    disable_editing = forms.ChoiceField(
        label="Desabilitar edição do e-mail e do assunto pelos ativistas?",
        choices=((True, "Desabilitar"), (False, "Habilitar")),
        widget=RadioSelect,
        initial=True,
    )

    sharing = forms.MultipleChoiceField(
        label="Opções de compartilhamento",
        choices=SharingChoices.choices,
        widget=CheckboxSelectMultiple,
    )

    class Meta:
        model = Pressure
        fields = "__all__"

    def save(self, commit):
        obj = super(PressureSettingsForm, self).save(commit)
        # Update Widget Settings
        if obj.widget:
            widget = BondeWidget.objects.get(id=obj.widget)
            new_settings = widget.settings or {}

            new_settings["sender_name"] = obj.sender_name
            new_settings["sender_email"] = obj.sender_email
            new_settings["email_subject"] = obj.thank_email_subject
            new_settings["email_body"] = obj.thank_email_body

            new_settings["disable_edit_field"] = "s" if obj.disable_editing else "n"

            if obj.submissions_limit and obj.submissions_interval:
                new_settings["optimization_enabled"] = True
                new_settings["mail_limit"] = obj.submissions_limit
                new_settings["batch_limit"] = obj.submissions_interval
            else:
                new_settings["optimization_enabled"] = False

            new_settings["pressure_body"] = obj.email_body
            if len(json.loads(obj.email_subject)) == 1:
                new_settings["pressure_subject"] = json.loads(obj.email_subject)[0]
            else:
                new_settings["pressure_subject"] = None

            if obj.targetgroup_set.count() == 1:
                new_settings["targets"] = list(
                    map(
                        lambda x: f"{x.name} <{x.email}>",
                        obj.targetgroup_set.first().targets.all(),
                    )
                )

            widget.settings = new_settings
            widget.save()

        return obj
