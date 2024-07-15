from django import forms
from captcha.widgets import ReCaptchaV2Checkbox

from django_select2.forms import Select2Widget
from django.utils.functional import lazy
from django.urls import reverse_lazy

from .fields import ValidateOnceReCaptchaField
from .locations_utils import get_ufs, get_choices


class CaptchaForm(forms.Form):
    captcha = ValidateOnceReCaptchaField(widget=ReCaptchaV2Checkbox())


class InitialForm(forms.Form):
    legal_name = forms.CharField(label="Nome")
    ballot_name = forms.CharField(label="Nome na urna")
    birth_date = forms.DateField(label="Data de nascimento")
    email = forms.EmailField(label="E-mail")
    cpf_cnpj = forms.CharField(label="CPF/CNPJ")
    tse_id = forms.CharField(label="Identificação TSE (?)", required=False)


class ApplicationForm(forms.Form):
    number_id = forms.IntegerField(label="Número de identificação", min_value=1)
    intended_position = forms.CharField(label="Cargo pretendido")
    state = forms.ChoiceField(
        label="Estado",
        choices=lazy(get_ufs, list)(),
        widget=Select2Widget(
            attrs={
                "data-address-fields": "state",
                "data-address-url": reverse_lazy("address"),
            }
        )
    )
    city = forms.ChoiceField(
        choices=[],
        label="Cidade",
        widget=Select2Widget(
            attrs={
                "data-address-fields": "city",
                "data-address-url": reverse_lazy("address"),
            }
        )
    )
    is_collective_mandate = forms.BooleanField(
        label="É um mandato coletivo?", required=False
    )
    political_party = forms.CharField(label="Partido político")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'state' in self.data:
            self.fields['city'].choices = get_choices(self.data.get('state'))
        elif self.initial.get('state'):
            self.fields['city'].choices = get_choices(self.initial.get('state'))
    class Media:
        css = {
            "all": [
                "https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css",
            ]
        }
        js = [
            "https://code.jquery.com/jquery-3.5.1.min.js",
            "https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.full.min.js",
            "https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/i18n/pt-BR.js",
            "js/address-fields.js",
        ]

class ProfileForm(forms.Form):
    video = forms.URLField(label="Vídeo", required=False)
    photo = forms.URLField(label="Foto", required=False)
    gender = forms.CharField(label="Gênero")
    color = forms.CharField(label="Raça")
    sexuality = forms.CharField(label="Sexualidade", required=False)


class TrackForm(forms.Form):
    education = forms.CharField(label="Escolaridade", required=False)
    employment = forms.CharField(label="Ocupação", required=False)
    short_description = forms.CharField(label="Minibio", widget=forms.Textarea())


class FlagForm(forms.Form):
    is_renewable_energy = forms.BooleanField(label="Energia Renovável", required=False)
    is_transport_and_mobility = forms.BooleanField(label="Transporte e Mobilidade", required=False)


class AppointmentForm(forms.Form):
    appointment_1 = forms.BooleanField(label="Compromisso 1", required=False)
    appointment_2 = forms.BooleanField(label="Compromisso 2", required=False)


class CheckoutForm(forms.Form):
    is_valid = forms.BooleanField()


register_form_list = [
    ("captcha", CaptchaForm),
    ("informacoes-iniciais", InitialForm),
    ("informacoes-de-candidatura", ApplicationForm),
    ("complemente-seu-perfil", ProfileForm),
    ("sobre-sua-trajetoria", TrackForm),
    ("bandeiras-da-sua-candidatura", FlagForm),
    ("compromissos", AppointmentForm),
    ("checkout", CheckoutForm)
]