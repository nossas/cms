from django import forms
from django.core.exceptions import ValidationError
from django.utils.functional import lazy

from captcha.widgets import ReCaptchaV2Checkbox
from entangled.forms import EntangledModelFormMixin
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, HTML
from bootstrap_datepicker_plus.widgets import DatePickerInput

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
    CheckboxSelectMultipleWidget,
    ValidateOnceReCaptchaField,
    CheckboxTextField,
    InlineArrayField,
    CepField,
    ToggleButtonField,
    VideoField,
    InputMask,
    HTMLBooleanField,
)
from .layout import NoCrispyField, FileField


class DisabledMixin:

    def __init__(self, disabled=False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if disabled:
            self.disabled = disabled
            for field_name in self.fields:
                self.fields[field_name].widget.attrs.update(
                    {"readonly": True, "disabled": True}
                )


class CaptchaForm(EntangledModelFormMixin, forms.ModelForm):
    captcha = ValidateOnceReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        # Sobrescreve o template na view para criar uma página customizada
        model = CandidatureFlow
        entangled_fields = {"properties": ["captcha"]}
        untangled_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["captcha"].label = ""


class AppointmentForm(EntangledModelFormMixin, DisabledMixin, forms.ModelForm):
    appointment_1 = ToggleButtonField(
        icon_name="ds-icon-wrapper-2",
        text_html="""
<span class='fw-semibold'>Aliquam porta libero et ligula euismod sodales.</span>
<span class='form-text'>Vestibulum quis sapien mattis, porta diam quis, scelerisque neque. Integer id nisi in sem viverra mattis sit amet sit amet quam.</span>
""",
    )
    appointment_2 = ToggleButtonField(
        icon_name="ds-icon-wrapper",
        text_html="""
<span class='fw-semibold'>Aliquam porta libero et ligula euismod sodales.</span>
<span class='form-text'>Vestibulum quis sapien mattis, porta diam quis, scelerisque neque. Integer id nisi in sem viverra mattis sit amet sit amet quam.</span>
""",
    )

    class Meta:
        title = "Você assume compromisso com..."
        description = "Esses são os compromissos climáticos que todos os candidatos devem assumir ao criar um perfil no Vote pelo Clima. Eles ficarão visíveis aos eleitores, mostrando seu empenho em um futuro sustentável."
        model = CandidatureFlow
        entangled_fields = {"properties": ["appointment_1", "appointment_2"]}
        untangled_fields = []


class PersonalForm(EntangledModelFormMixin, DisabledMixin, forms.ModelForm):
    legal_name = forms.CharField(
        label="Nome",
        help_text="Nome da pessoa que possui os dados registrados no TSE.",
        widget=forms.TextInput(attrs={"placeholder": "Digite seu nome completo"}),
    )
    ballot_name = forms.CharField(
        label="Nome na urna",
        help_text="Nome público, registrado no TSE.",
        widget=forms.TextInput(
            attrs={"placeholder": "Digite o nome que aparecerá na urna"}
        ),
    )
    birth_date = forms.DateField(
        label="Data de nascimento",
        widget=DatePickerInput(
            attrs={"placeholder": "dd/mm/yyyy"},
            options={"locale": "pt-BR", "format": "DD/MM/YYYY"},
        ),
        localize="pt-BR",
    )
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={"placeholder": "Digite seu e-mail"}),
    )
    cpf = forms.CharField(
        label="CPF",
        help_text="CPF é necessário para confirmar sua identidade junto ao TSE",
        widget=InputMask(
            mask="000.000.000-00", attrs={"placeholder": "Digite seu CPF"}
        ),
    )

    class Meta:
        title = "Informações pessoais"
        description = "Vamos lá! Essas informações são essenciais para verificar sua candidatura e garantir a segurança. Se for uma candidatura coletiva, a pessoa responsável deve ter os dados registrados no TSE."
        model = CandidatureFlow
        entangled_fields = {
            "properties": ["legal_name", "ballot_name", "birth_date", "email", "cpf"]
        }
        untangled_fields = []

    class Media:
        js = ["https://code.jquery.com/jquery-3.5.1.min.js"]

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
                style="grid-row-gap:0;",
            )
        )


class ApplicationForm(EntangledModelFormMixin, DisabledMixin, forms.ModelForm):
    number_id = forms.IntegerField(
        label="Número de identificação",
        min_value=1,
        help_text="Número fornecido pelo TSE",
        widget=forms.NumberInput(
            attrs={"placeholder": "Digite seu número de identificação"}
        ),
    )
    intended_position = forms.ChoiceField(
        label="Cargo pretendido",
        choices=IntendedPosition.choices,
        help_text="Selecione o cargo que você está concorrendo",
    )
    state = CepField(
        field="state",
        label="Estado",
        placeholder="Selecione",
        choices=[("", "Selecione")] + lazy(get_ufs, list)(),
        help_text="Estado onde você está concorrendo",
    )
    city = CepField(
        field="city",
        parent="state",
        label="Cidade",
        placeholder="Selecione",
        help_text="Cidade onde você está concorrendo",
    )
    is_collective_mandate = forms.BooleanField(
        label="É um mandato coletivo?",
        required=False,
        initial=False,
        widget=forms.RadioSelect(choices=((True, "Sim"), (False, "Não"))),
    )
    political_party = forms.ChoiceField(
        label="Partido político", choices=PoliticalParty.choices
    )
    deputy_mayor = forms.CharField(
        label="Nome vice-prefeitura",
        widget=forms.TextInput(attrs={"placeholder": "Digite o nome"}),
        required=False,
    )
    deputy_mayor_political_party = forms.ChoiceField(
        label="Partido político", choices=PoliticalParty.choices, required=False
    )

    class Meta:
        title = "Informações de candidatura"
        description = "Preencha os detalhes sobre sua candidatura."
        model = CandidatureFlow
        entangled_fields = {
            "properties": [
                "number_id",
                "intended_position",
                "state",
                "city",
                "is_collective_mandate",
                "political_party",
                "deputy_mayor",
                "deputy_mayor_political_party"
            ]
        }
        untangled_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        # TODO: investigar porque quando usamos layout o select2 duplica o campo
        self.helper.layout = Layout(
            Div(
                Div(Field("number_id"), css_class="g-col-12 g-col-md-6"),
                Div(Field("intended_position"), css_class="g-col-12 g-col-md-6"),
                Div(Field("state"), css_class="g-col-12 g-col-md-6"),
                Div(Field("city"), css_class="g-col-12 g-col-md-6"),
                Div(
                    NoCrispyField("is_collective_mandate"),
                    css_class="g-col-12 g-col-md-6 mb-3",
                ),
                Div(Field("political_party"), css_class="g-col-12 g-col-md-6"),
                Div(
                    HTML(
                        """
                        <hr/>
                        <h5>Informações vice-prefeitura</h5>
                        <p>Adicione informações somente em caso de candidaturas para prefeitura<p>
                        """
                    ),
                    css_class="g-col-12 g-col-md-12",
                ),
                Div(Field("deputy_mayor"), css_class="g-col-12 g-col-md-6"),
                Div(
                    Field("deputy_mayor_political_party"),
                    css_class="g-col-12 g-col-md-6",
                ),
                css_class="grid",
                style="grid-row-gap:0;",
            )
        )
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

    def clean(self):
        cleaned_data = super().clean()
        intended_position = cleaned_data.get("intended_position")
        deputy_mayor = cleaned_data.get("deputy_mayor")
        deputy_mayor_political_party = cleaned_data.get("deputy_mayor_political_party")

        if intended_position == IntendedPosition.prefeitura and not deputy_mayor:
            self.add_error("deputy_mayor", "Esse campo é obrigatório")

        if (
            intended_position == IntendedPosition.prefeitura
            and not deputy_mayor_political_party
        ):
            self.add_error("deputy_mayor_political_party", "Esse campo é obrigatório")


propose_text_label = "Proposta"
propose_text_help_text = (
    "Descreva sua proposta de forma clara e objetiva. Máximo de 300 caracteres."
)


class ProposeForm(EntangledModelFormMixin, DisabledMixin, forms.ModelForm):
    energia_renovavel = CheckboxTextField(
        checkbox_label="Energia Renovável",
        text_label=propose_text_label,
        text_help_text=propose_text_help_text,
        required=False,
    )
    transporte_e_mobilidade = CheckboxTextField(
        checkbox_label="Transporte e Mobilidade",
        text_label=propose_text_label,
        text_help_text=propose_text_help_text,
        required=False,
    )
    agricultura_sustentavel = CheckboxTextField(
        checkbox_label="Agricultura Sustentável",
        text_label=propose_text_label,
        text_help_text=propose_text_help_text,
        required=False,
    )
    conservacao_e_florestas = CheckboxTextField(
        checkbox_label="Conservação e Florestas",
        text_label=propose_text_label,
        text_help_text=propose_text_help_text,
        required=False,
    )
    gestao_de_residuos = CheckboxTextField(
        checkbox_label="Gestão de Resíduos",
        text_label=propose_text_label,
        text_help_text=propose_text_help_text,
        required=False,
    )
    agua_e_saneamento = CheckboxTextField(
        checkbox_label="Água e Saneamento",
        text_label=propose_text_label,
        text_help_text=propose_text_help_text,
        required=False,
    )
    empregos_verdes = CheckboxTextField(
        checkbox_label="Empregos Verdes",
        text_label=propose_text_label,
        text_help_text=propose_text_help_text,
        required=False,
    )
    mercados_e_financas = CheckboxTextField(
        checkbox_label="Mercados e finanças",
        text_label=propose_text_label,
        text_help_text=propose_text_help_text,
        required=False,
    )
    urbanismo_e_direito_a_cidade = CheckboxTextField(
        checkbox_label="Urbanismo e Direito à Cidade",
        text_label=propose_text_label,
        text_help_text=propose_text_help_text,
        required=False,
    )
    combate_ao_racismo_ambiental = CheckboxTextField(
        checkbox_label="Combate ao Racismo Ambiental",
        text_label=propose_text_label,
        text_help_text=propose_text_help_text,
        required=False,
    )
    direitos_indigenas = CheckboxTextField(
        checkbox_label="Direitos Indígenas",
        text_label=propose_text_label,
        text_help_text=propose_text_help_text,
        required=False,
    )
    saude_e_clima = CheckboxTextField(
        checkbox_label="Saúde e Clima",
        text_label=propose_text_label,
        text_help_text=propose_text_help_text,
        required=False,
    )
    adaptacao_climatica = CheckboxTextField(
        checkbox_label="Adaptação Climática",
        text_label=propose_text_label,
        text_help_text=propose_text_help_text,
        required=False,
    )

    class Meta:
        title = "Suas propostas"
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
        elif selected_size == 0:
            raise ValidationError("Selecione ao menos 1 bandeira")
        return cleaned_data


class TrackForm(EntangledModelFormMixin, DisabledMixin, forms.ModelForm):
    education = forms.ChoiceField(
        label="Escolaridade", required=False, choices=Education.choices
    )
    employment = forms.CharField(label="Ocupação", required=False)
    short_description = forms.CharField(
        label="Minibio",
        widget=forms.Textarea(attrs={"placeholder": "Escreva uma breve biografia"}),
        help_text="Fale um pouco sobre você e sua jornada até aqui. Até 800 caracteres.",
    )
    milestones = InlineArrayField(
        forms.CharField(max_length=140, required=False),
        required=False,
        label="Histórico de atuação",
        item_label="Realização",
        add_button_text="ADICIONAR MARCO",
        help_text="Adicione momentos e realizações marcantes da sua trajetória.",
        placeholder="Recebi o Prêmio XYZ pela Iniciativa Ambiental",
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
                style="grid-row-gap:0;",
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
                Div(FileField("photo"), css_class="g-col-12 g-col-md-6"),
                Div(FileField("video"), css_class="g-col-12 g-col-md-6"),
                Div(Field("gender"), css_class="g-col-12 g-col-md-6"),
                Div(Field("color"), css_class="g-col-12 g-col-md-6"),
                Div(Field("sexuality"), css_class="g-col-12 g-col-md-6"),
                Div(Field("social_media"), css_class="g-col-12"),
                css_class="grid",
                style="grid-row-gap:0;",
            )
        )


class CheckoutForm(EntangledModelFormMixin, DisabledMixin, forms.ModelForm):
    is_valid = HTMLBooleanField(
        label="Ao preencher o formulário e se cadastrar na Campanha, você está ciente de que seus dados pessoais serão tratados de acordo com o <a href='#' target='blank'>Aviso de Privacidade</a>."
    )

    class Meta:
        title = "Para finalizar, confirme suas informações"
        model = CandidatureFlow
        entangled_fields = {"properties": ["is_valid"]}
        untangled_fields = []


register_form_list = [
    ("captcha", CaptchaForm),
    ("compromissos", AppointmentForm),
    ("informacoes-pessoais", PersonalForm),
    ("informacoes-de-candidatura", ApplicationForm),
    ("suas-propostas", ProposeForm),
    ("sobre-sua-trajetoria", TrackForm),
    ("complemente-seu-perfil", ProfileForm),
    ("checkout", CheckoutForm),
]

class CandidatureSearchTopForm(forms.Form):
    state = forms.ChoiceField(choices=[('', 'Estado')] + get_ufs(), required=False)
    city = forms.ChoiceField(choices=[('', 'Cidade')], required=False)
    intended_position = forms.ChoiceField(choices=IntendedPosition.choices, required=False)
    political_party = forms.ChoiceField(choices=PoliticalParty.choices, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    def update_city_choices(self, state):
        if state:
            self.fields['city'].choices = get_choices(state)
        else:
            self.fields['city'].choices = [('', 'Cidade')]

class CandidatureSearchSideForm(forms.Form):
    gender = forms.MultipleChoiceField(
        choices=Gender.choices[1:], 
        required=False, 
        widget=CheckboxSelectMultipleWidget(),
        label='Gênero'
    )
    color = forms.MultipleChoiceField(
        choices=Color.choices[1:], 
        required=False, 
        widget=CheckboxSelectMultipleWidget(),
        label='Raça'
    )
    sexuality = forms.MultipleChoiceField(
        choices=Sexuality.choices[1:], 
        required=False, 
        widget=CheckboxSelectMultipleWidget(),
        label='Sexualidade'
    )
    # proposes = forms.MultipleChoiceField(
    ballot_name = forms.CharField(required=False)
    keyword = forms.CharField(required=False)
    is_collective_mandate = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False