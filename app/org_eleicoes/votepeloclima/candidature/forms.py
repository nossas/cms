from django import forms
from captcha.widgets import ReCaptchaV2Checkbox

from .fields import (
    ValidateOnceReCaptchaField,
    StateCepField,
    CityCepField,
    CheckboxTextWidget,
)


class DisabledMixin:

    def __init__(self, disabled=False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if disabled:
            # import ipdb;ipdb.set_trace()
            for field_name in self.fields:
                self.fields[field_name].widget.attrs.update(
                    {"readonly": True, "disabled": True}
                )


class CaptchaForm(forms.Form):
    captcha = ValidateOnceReCaptchaField(widget=ReCaptchaV2Checkbox())


class InitialForm(DisabledMixin, forms.Form):
    legal_name = forms.CharField(label="Nome")
    ballot_name = forms.CharField(label="Nome na urna")
    birth_date = forms.DateField(label="Data de nascimento")
    email = forms.EmailField(label="E-mail")
    cpf_cnpj = forms.CharField(label="CPF/CNPJ")
    tse_id = forms.CharField(label="Identificação TSE (?)", required=False)

    class Meta:
        title = "Informações iniciais"


class ApplicationForm(DisabledMixin, forms.Form):
    number_id = forms.IntegerField(label="Número de identificação", min_value=1)
    intended_position = forms.CharField(label="Cargo pretendido")
    state = StateCepField(label="Estado")
    city = CityCepField(label="Cidade")
    is_collective_mandate = forms.BooleanField(
        label="É um mandato coletivo?", required=False
    )
    political_party = forms.CharField(label="Partido político")
    
    class Meta:
        title = "Informações de candidatura"


class ProfileForm(DisabledMixin, forms.Form):
    video = forms.URLField(label="Vídeo", required=False)
    photo = forms.URLField(label="Foto", required=False)
    gender = forms.CharField(label="Gênero")
    color = forms.CharField(label="Raça")
    sexuality = forms.CharField(label="Sexualidade", required=False)

    class Meta:
        title = "Complemente seu perfil"


class TrackForm(DisabledMixin, forms.Form):
    education = forms.CharField(label="Escolaridade", required=False)
    employment = forms.CharField(label="Ocupação", required=False)
    short_description = forms.CharField(label="Minibio", widget=forms.Textarea())

    class Meta:
        title = "Sobre sua trajetória"


class FlagForm(DisabledMixin, forms.Form):
    is_renewable_energy = forms.CharField(
        label="Energia Renovável", required=False, widget=CheckboxTextWidget()
    )
    is_transport_and_mobility = forms.CharField(
        label="Transporte e Mobilidade", required=False, widget=CheckboxTextWidget()
    )
    is_sustainable_agriculture = forms.CharField(
        label="Agricultura Sustentável", required=False, widget=CheckboxTextWidget()
    )

    class Meta:
        title = "Bandeiras da sua candidatura"


class AppointmentForm(DisabledMixin, forms.Form):
    appointment_1 = forms.BooleanField(label="Compromisso 1", required=False)
    appointment_2 = forms.BooleanField(label="Compromisso 2", required=False)

    class Meta:
        title = "Você assume compromisso com..."


class CheckoutForm(forms.Form):
    is_valid = forms.BooleanField()

    class Meta:
        title = "Para finalizar, confirme as suas informações"


register_form_list = [
    ("captcha", CaptchaForm),
    ("compromissos", AppointmentForm),
    ("informacoes-iniciais", InitialForm),
    ("informacoes-de-candidatura", ApplicationForm),
    ("complemente-seu-perfil", ProfileForm),
    ("sobre-sua-trajetoria", TrackForm),
    ("bandeiras-da-sua-candidatura", FlagForm),
    ("checkout", CheckoutForm),
]
