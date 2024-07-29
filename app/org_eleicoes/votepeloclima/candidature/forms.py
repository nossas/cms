from django import forms
from django.core.exceptions import ValidationError
from django.utils.functional import lazy

from captcha.widgets import ReCaptchaV2Checkbox
from entangled.forms import EntangledModelFormMixin
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field

from .locations_utils import get_ufs, get_choices
from .models import CandidatureFlow
from .fields import (
    ValidateOnceReCaptchaField,
    CheckboxTextField,
    InlineArrayField,
    VideoField,
    CepField,
)


class DisabledMixin:

    def __init__(self, disabled=False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if disabled:
            for field_name in self.fields:
                self.fields[field_name].widget.attrs.update(
                    {"readonly": True, "disabled": True}
                )


class CaptchaForm(EntangledModelFormMixin, forms.ModelForm):
    captcha = ValidateOnceReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        title = "Vamos começar?"
        model = CandidatureFlow
        entangled_fields = {"properties": ["captcha"]}
        untangled_fields = []


class AppointmentForm(EntangledModelFormMixin, DisabledMixin, forms.ModelForm):
    appointment_1 = forms.BooleanField(label="Compromisso 1", required=False)
    appointment_2 = forms.BooleanField(label="Compromisso 2", required=False)

    class Meta:
        title = "Você assume compromisso com..."
        model = CandidatureFlow
        entangled_fields = {"properties": ["appointment_1", "appointment_2"]}
        untangled_fields = []


class InitialForm(EntangledModelFormMixin, DisabledMixin, forms.ModelForm):
    legal_name = forms.CharField(label="Nome")
    ballot_name = forms.CharField(label="Nome na urna")
    birth_date = forms.DateField(label="Data de nascimento")
    email = forms.EmailField(label="E-mail")
    cpf = forms.CharField(label="CPF")

    class Meta:
        title = "Informações pessoais"
        model = CandidatureFlow
        entangled_fields = {
            "properties": ["legal_name", "ballot_name", "birth_date", "email", "cpf"]
        }
        untangled_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div(Field("legal_name"), css_class="g-col-12 g-col-md-6"),
                Div(Field("ballot_name"), css_class="g-col-12 g-col-md-6"),
                Div(Field("birth_date"), css_class="g-col-12 g-col-md-6"),
                Div(Field("email"), css_class="g-col-12 g-col-md-6"),
                Div(Field("cpf"), css_class="g-col-12 g-col-md-6"),
                css_class="grid",
            )
        )


class ApplicationForm(EntangledModelFormMixin, DisabledMixin, forms.ModelForm):
    number_id = forms.IntegerField(label="Número de identificação", min_value=1)
    intended_position = forms.CharField(label="Cargo pretendido")
    state = CepField(
        field="state",
        label="Estado",
        placeholder="Selecione seu estado",
        choices=lazy(get_ufs, list)(),
    )
    city = CepField(
        field="city", parent="state", label="Cidade", placeholder="Selecione sua cidade"
    )
    is_collective_mandate = forms.BooleanField(
        label="É um mandato coletivo?", required=False
    )
    political_party = forms.CharField(label="Partido político")

    class Meta:
        title = "Informações de candidatura"
        model = CandidatureFlow
        entangled_fields = {
            "properties": [
                "number_id",
                "intended_position",
                "state",
                "city",
                "is_collective_mandate",
                "political_party",
            ]
        }
        untangled_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        # TODO: investigar porque quando usamos layout o select2 duplica o campo
        # self.helper.layout = Layout(
        #     Div(
        #         Div(Field("number_id"), css_class="g-col-12 g-col-md-6"),
        #         Div(Field("intended_position"), css_class="g-col-12 g-col-md-6"),
        #         Div(Field("state"), css_class="g-col-12 g-col-md-6"),
        #         Div(Field("city"), css_class="g-col-12 g-col-md-6"),
        #         Div(Field("is_collective_mandate"), css_class="g-col-12 g-col-md-6"),
        #         Div(Field("political_party"), css_class="g-col-12 g-col-md-6"),
        #         css_class="grid",
        #     )
        # )
        data = kwargs.get("data", None)
        instance = kwargs.get("instance", None)

        if data or instance:
            state = None
            if instance:
                state = instance.properties.get("state", None)
            if data:
                state = data.get("informacoes-de-candidatura-state", None)

            if state:
                self.fields["city"].choices = get_choices(state)


class FlagForm(EntangledModelFormMixin, DisabledMixin, forms.ModelForm):
    is_renewable_energy = CheckboxTextField(
        checkbox_label="Energia Renovável",
        text_label="Proposta",
        help_text="Proin non nisl sed lorem pharetra blandit. Curabitur nec metus vitae libero elementum cursus. Suspendisse potenti. Praesent sit amet turpis vel lacus volutpat scelerisque. Proin non nisl sed lorem pharetra blandit.",
        required=False,
    )
    is_transport_and_mobility = CheckboxTextField(
        checkbox_label="Transporte e Mobilidade", text_label="Proposta", required=False
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
        title = "Bandeiras e propostas"
        model = CandidatureFlow
        entangled_fields = {
            "properties": [
                "is_renewable_energy",
                "is_transport_and_mobility",
                "is_sustainable_agriculture",
                "is_conservation_and_forests",
                "is_waste_management",
                "is_water_and_sanitation",
                "is_green_jobs",
                "is_markets_and_finance",
                "is_urbanism_and_the_right_to_the_city",
                "is_combating_environmental_racism",
                "is_sustainable_agriculture",
                "is_indigenous_rights",
                "is_health_and_climate",
                "is_climate_adaptation",
            ]
        }
        untangled_fields = []

    def clean(self):
        cleaned_data = super().clean()
        selected_size = len(list(filter(lambda x: bool(x), cleaned_data.values())))
        if selected_size > 5:
            raise ValidationError("Selecione apenas 5 bandeiras")
        return cleaned_data


class TrackForm(EntangledModelFormMixin, DisabledMixin, forms.ModelForm):
    education = forms.CharField(label="Escolaridade", required=False)
    employment = forms.CharField(label="Ocupação", required=False)
    short_description = forms.CharField(label="Minibio", widget=forms.Textarea())
    milestones = InlineArrayField(
        forms.CharField(max_length=140, required=False),
        required=False,
        label="Histórico de atuação",
        item_label="Realização",
        add_button_text="Adicionar outra realização",
        help_text="Adicione momentos e realizações marcantes da sua trajetória.",
    )

    def clean_milestones(self):
        value = self.cleaned_data["milestones"]
        return value

    class Meta:
        title = "Sobre sua trajetória"
        model = CandidatureFlow
        entangled_fields = {
            "properties": [
                "education",
                "employment",
                "short_description",
                "milestones",
            ]
        }
        untangled_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div(Field("education"), css_class="g-col-12 g-col-md-6"),
                Div(Field("employment"), css_class="g-col-12 g-col-md-6"),
                Div(Field("short_description"), css_class="g-col-12"),
                Div(Field("milestones"), css_class="g-col-12"),
                css_class="grid",
            )
        )


class ProfileForm(EntangledModelFormMixin, DisabledMixin, forms.ModelForm):
    video = VideoField(label="Vídeo", required=False)
    photo = forms.ImageField(label="Foto", required=False)
    gender = forms.CharField(label="Gênero")
    color = forms.CharField(label="Raça")
    sexuality = forms.CharField(label="Sexualidade", required=False)
    social_media = InlineArrayField(
        forms.URLField(required=False),
        required=False,
        label="Redes sociais",
        item_label="Rede social",
        add_button_text="Adicionar outra rede social",
        help_text="Conecte suas redes sociais para ampliar sua visibilidade e engajamento com os eleitores.",
    )

    def clean_social_media(self):
        value = self.cleaned_data["social_media"]
        return value

    class Meta:
        title = "Complemente seu perfil"
        model = CandidatureFlow
        entangled_fields = {
            "properties": [
                "gender",
                "color",
                "sexuality",
                "social_media",
            ]
        }
        untangled_fields = [
            "video",
            "photo",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div(Field("photo"), css_class="g-col-12 g-col-md-6"),
                Div(Field("video"), css_class="g-col-12 g-col-md-6"),
                Div(Field("gender"), css_class="g-col-12 g-col-md-6"),
                Div(Field("color"), css_class="g-col-12 g-col-md-6"),
                Div(Field("sexuality"), css_class="g-col-12 g-col-md-6"),
                Div(Field("social_media"), css_class="g-col-12"),
                css_class="grid",
            )
        )


class CheckoutForm(EntangledModelFormMixin, DisabledMixin, forms.ModelForm):
    is_valid = forms.BooleanField()

    class Meta:
        title = "Para finalizar, confirme suas informações"
        model = CandidatureFlow
        entangled_fields = {"properties": ["is_valid"]}
        untangled_fields = []


register_form_list = [
    ("captcha", CaptchaForm),
    ("compromissos", AppointmentForm),
    ("informacoes-iniciais", InitialForm),
    ("informacoes-de-candidatura", ApplicationForm),
    ("bandeiras-da-sua-candidatura", FlagForm),
    ("sobre-sua-trajetoria", TrackForm),
    ("complemente-seu-perfil", ProfileForm),
    ("checkout", CheckoutForm),
]
