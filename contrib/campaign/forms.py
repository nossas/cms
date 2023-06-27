import json

from django import forms
from django_select2 import forms as s2forms
# from django.utils.functional import lazy

from contrib.bonde.models import Widget as BondeWidget

from .models import Pressure


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


# class BondeSearchWidget(s2forms.Select2Widget):
#     model = BondeWidget
#     search_fields = [
#         "block__mobilization__name__icontains"
#     ]

#     def get_queryset(self):
#         return self.model.objects.on_site().filter(kind="pressure")

#     def filter_queryset(self, request, term, queryset=None, **dependent_fields):
#         return self.get_queryset().filter(block__mobilization__name__icontains=term)


class BondeWidgetSelectWidget(s2forms.Select2Widget):
    empty_label = "Busque pelo nome ou pelo id da widget"


def get_choices():
    qs = BondeWidget.objects.on_site().filter(kind="pressure")

    return list(
        map(lambda x: (x.id, f"{x.block.mobilization.name} ({x.id})"), qs.all())
    )


class PressureSettingsForm(forms.ModelForm):
    widget_id = forms.ChoiceField(
        label="Selecione o form de pressão criado no BONDE",
        choices=get_choices,
        widget=BondeWidgetSelectWidget,
        required=False
    )

    class Meta:
        model = Pressure
        fields = ["widget_id"]

    class Media:
        js = ("//ajax.googleapis.com/ajax/libs/jquery/3.7.0/jquery.min.js",)
