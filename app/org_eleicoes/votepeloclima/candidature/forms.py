from django import forms
from django.core.exceptions import ValidationError
from django.utils.functional import lazy

from captcha.widgets import ReCaptchaV2Checkbox
from entangled.forms import EntangledModelFormMixin
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field

from .locations_utils import get_ufs, get_choices
from .choices import (
    PoliticalParty,
    IntendedPosition,
    Education,
    Color,
    Gender,
    Sexuality,
)
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
    intended_position = forms.ChoiceField(
        label="Cargo pretendido", choices=IntendedPosition.choices
    )
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
    political_party = forms.ChoiceField(
        label="Partido político", choices=PoliticalParty.choices
    )

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
    energia_renovavel = CheckboxTextField(
        checkbox_label="Energia Renovável",
        text_label="Proposta",
        help_text="Proin non nisl sed lorem pharetra blandit. Curabitur nec metus vitae libero elementum cursus. Suspendisse potenti. Praesent sit amet turpis vel lacus volutpat scelerisque. Proin non nisl sed lorem pharetra blandit.",
        required=False,
    )
    transporte_e_mobilidade = CheckboxTextField(
        checkbox_label="Transporte e Mobilidade", text_label="Proposta", required=False
    )
    agricultura_sustentavel = CheckboxTextField(
        checkbox_label="Agricultura Sustentável",
        text_label="Proposta",
        required=False,
    )
    conservacao_e_florestas = CheckboxTextField(
        checkbox_label="Conservação e Florestas",
        text_label="Proposta",
        required=False,
    )
    gestao_de_residuos = CheckboxTextField(
        checkbox_label="Gestão de Resíduos",
        text_label="Proposta",
        required=False,
    )
    agua_e_saneamento = CheckboxTextField(
        checkbox_label="Água e Saneamento",
        text_label="Proposta",
        required=False,
    )
    empregos_verdes = CheckboxTextField(
        checkbox_label="Empregos Verdes",
        text_label="Proposta",
        required=False,
    )
    mercados_e_financas = CheckboxTextField(
        checkbox_label="Mercados e finanças",
        text_label="Proposta",
        required=False,
    )
    urbanismo_e_direito_a_cidade = CheckboxTextField(
        checkbox_label="Urbanismo e Direito à Cidade",
        text_label="Proposta",
        required=False,
    )
    combate_ao_racismo_ambiental = CheckboxTextField(
        checkbox_label="Combate ao Racismo Ambiental",
        text_label="Proposta",
        required=False,
    )
    direitos_indigenas = CheckboxTextField(
        checkbox_label="Direitos Indígenas",
        text_label="Proposta",
        required=False,
    )
    saude_e_clima = CheckboxTextField(
        checkbox_label="Saúde e Clima",
        text_label="Proposta",
        required=False,
    )
    adaptacao_climatica = CheckboxTextField(
        checkbox_label="Adaptação Climática",
        text_label="Proposta",
        required=False,
    )

    class Meta:
        title = "Bandeiras e propostas"
        model = CandidatureFlow
        entangled_fields = {
            "properties": [
                "energia_renovavel",
                "transporte_e_mobilidade",
                "agricultura_sustentavel",
                "conservacao_e_florestas",
                "gestao_de_residuos",
                "agua_e_saneamento",
                "empregos_verdes",
                "mercados_e_financas",
                "urbanismo_e_direito_a_cidade",
                "combate_ao_racismo_ambiental",
                "direitos_indigenas",
                "saude_e_clima",
                "adaptacao_climatica",
            ]
        }
        untangled_fields = []

    def clean(self):
        cleaned_data = super().clean()
        selected_size = len(list(filter(lambda x: bool(x), cleaned_data.values())))
        if selected_size > 3:
            raise ValidationError("Selecione apenas 3 bandeiras")
        return cleaned_data


class TrackForm(EntangledModelFormMixin, DisabledMixin, forms.ModelForm):
    education = forms.ChoiceField(
        label="Escolaridade", required=False, choices=Education.choices
    )
    employment = forms.CharField(label="Ocupação", required=False)
    short_description = forms.CharField(
        label="Minibio",
        widget=forms.Textarea(),
        help_text="Fale um pouco sobre você e sua jornada até aqui. Até 800 caracteres.",
    )
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
    photo = forms.ImageField(label="Foto")
    gender = forms.ChoiceField(label="Gênero", choices=Gender.choices)
    color = forms.ChoiceField(label="Raça", choices=Color.choices)
    sexuality = forms.ChoiceField(
        label="Sexualidade", required=False, choices=Sexuality.choices
    )
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
    is_valid = forms.BooleanField(
        label="Ao preencher o formulário e se cadastrar na Campanha, você está ciente de que seus dados pessoais serão tratados de acordo com o Aviso de Privacidade."
    )

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
