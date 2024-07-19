from django import forms
from django.contrib.postgres.forms import SimpleArrayField
from django.core.exceptions import ValidationError

from captcha.widgets import ReCaptchaV2Checkbox

from .fields import (
    ValidateOnceReCaptchaField,
    StateCepField,
    CityCepField,
    CheckboxTextField,
    InlineArrayWidget,
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
    social_media = SimpleArrayField(forms.URLField(), widget=InlineArrayWidget())

    class Meta:
        title = "Complemente seu perfil"


class TrackForm(DisabledMixin, forms.Form):
    education = forms.CharField(label="Escolaridade", required=False)
    employment = forms.CharField(label="Ocupação", required=False)
    short_description = forms.CharField(label="Minibio", widget=forms.Textarea())
    milestones = SimpleArrayField(forms.CharField(max_length=140), widget=InlineArrayWidget())

    class Meta:
        title = "Sobre sua trajetória"


class FlagForm(DisabledMixin, forms.Form):
    is_renewable_energy = CheckboxTextField(
        checkbox_label="Energia Renovável",
        text_label="Proposta",
        help_text="Proin non nisl sed lorem pharetra blandit. Curabitur nec metus vitae libero elementum cursus. Suspendisse potenti. Praesent sit amet turpis vel lacus volutpat scelerisque. Proin non nisl sed lorem pharetra blandit.",
        required=False
    )
    is_transport_and_mobility = CheckboxTextField(
        checkbox_label="Transporte e Mobilidade",
        text_label="Proposta",
        required=False
    )
    is_sustainable_agriculture = CheckboxTextField(
        checkbox_label="Agricultura Sustentável",
        text_label="Proposta",
        required=False,
    )
    is_conservation_and_forests = CheckboxTextField(
        checkbox_label="Conservação e Florestas",
        text_label="Proposta",
        required=False,
    )
    is_waste_management = CheckboxTextField(
        checkbox_label="Gestão de Resíduos",
        text_label="Proposta",
        required=False,
    )
    is_water_and_sanitation = CheckboxTextField(
        checkbox_label="Água e Saneamento",
        text_label="Proposta",
        required=False,
    )
    is_green_jobs = CheckboxTextField(
        checkbox_label="Empregos Verdes",
        text_label="Proposta",
        required=False,
    )
    is_markets_and_finance = CheckboxTextField(
        checkbox_label="Mercados e finanças",
        text_label="Proposta",
        required=False,
    )
    is_urbanism_and_the_right_to_the_city = CheckboxTextField(
        checkbox_label="Urbanismo e Direito à Cidade",
        text_label="Proposta",
        required=False,
    )
    is_combating_environmental_racism = CheckboxTextField(
        checkbox_label="Combate ao Racismo Ambiental",
        text_label="Proposta",
        required=False,
    )
    is_sustainable_agriculture = CheckboxTextField(
        checkbox_label="Agricultura Sustentável",
        text_label="Proposta",
        required=False,
    )
    is_indigenous_rights = CheckboxTextField(
        checkbox_label="Direitos Indígenas",
        text_label="Proposta",
        required=False,
    )
    is_health_and_climate = CheckboxTextField(
        checkbox_label="Saúde e Clima",
        text_label="Proposta",
        required=False,
    )
    is_climate_adaptation = CheckboxTextField(
        checkbox_label="Adaptação Climática",
        text_label="Proposta",
        required=False,
    )

    class Meta:
        title = "Bandeiras da sua candidatura"
    
    def clean(self):
        cleaned_data = super().clean()
        selected_size = len(list(filter(lambda x: bool(x), cleaned_data.values())))
        if selected_size > 5:
            raise ValidationError("Selecione apenas 5 bandeiras")
        return cleaned_data


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
