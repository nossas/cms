from django import forms
from captcha.widgets import ReCaptchaV2Checkbox

from .fields import ValidateOnceReCaptchaField


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
    state = forms.CharField(label="Estado")
    city = forms.CharField(label="Cidade")
    is_collective_mandate = forms.BooleanField(
        label="É um mandato coletivo?", required=False
    )
    political_party = forms.CharField(label="Partido político")


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