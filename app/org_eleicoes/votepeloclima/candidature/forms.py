from django import forms
from django.core.exceptions import ValidationError
from django.utils.functional import lazy
from django.templatetags.static import static

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
        icon_name="ds-icon-compromisso-1",
        text_html="Políticas de adaptação das cidades para reduzir tragédias",
    )
    appointment_2 = ToggleButtonField(
        icon_name="ds-icon-compromisso-2",
        text_html="Políticas para redução de emissões e transição energética",
    )
    appointment_3 = ToggleButtonField(
        icon_name="ds-icon-compromisso-3",
        text_html="Políticas sociais de apoio às populações atingidas",
    )
    appointment_4 = ToggleButtonField(
        icon_name="ds-icon-compromisso-4",
        text_html="Transição climática com justiça social, racial e de gênero",
    )
    appointment_5 = ToggleButtonField(
        icon_name="ds-icon-compromisso-5",
        text_html="Proteção ambiental e de recursos naturais",
    )
    appointment_6 = ToggleButtonField(
        icon_name="ds-icon-compromisso-6",
        text_html="Incentivo à participação popular e ao engajamento da juventude",
    )
    appointment_7 = ToggleButtonField(
        icon_name="ds-icon-compromisso-7",
        text_html="Investimentos em pesquisa e inovação para enfrentar a crise climática",
    )
    appointment_8 = ToggleButtonField(
        icon_name="ds-icon-compromisso-8",
        text_html="Valorização de saberes tradicionais e tecnologias sociais na busca de soluções",
    )

    class Meta:
        title = "Você assume compromisso com..."
        description = "Esses são os valores e princípios básicos que todos os candidatos devem assumir ao criar um perfil no Vote pelo Clima. Eles representam compromissos essenciais e serão visíveis aos eleitores, evidenciando sua dedicação a um futuro sustentável. Para continuar, é necessário selecionar todos os compromissos."
        model = CandidatureFlow
        entangled_fields = {
            "properties": [
                "appointment_1",
                "appointment_2",
                "appointment_3",
                "appointment_4",
                "appointment_5",
                "appointment_6",
                "appointment_7",
                "appointment_8",
            ]
        }
        untangled_fields = []


class PersonalForm(EntangledModelFormMixin, DisabledMixin, forms.ModelForm):
    legal_name = forms.CharField(
        label="Nome",
        widget=forms.TextInput(attrs={"placeholder": "Digite seu nome completo"}),
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
    birth_date = forms.DateField(
        label="Data de nascimento",
        widget=DatePickerInput(
            attrs={"placeholder": "dd/mm/yyyy"},
            options={"locale": "pt-BR", "format": "DD/MM/YYYY"},
        ),
        localize="pt-BR",
    )
    
    class Meta:
        title = "Informações pessoais"
        description = "Vamos lá! Essas informações são essenciais para verificar sua candidatura e garantir a segurança. Se for uma candidatura coletiva, a pessoa responsável deve ter os dados registrados no TSE."
        model = CandidatureFlow
        entangled_fields = {
            "properties": ["legal_name", "email", "cpf", "birth_date"]
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
                Div(Field("email"), css_class="g-col-12 g-col-md-6"),
                Div(Field("cpf"), css_class="g-col-12 g-col-md-6"),
                Div(Field("birth_date"), css_class="g-col-12 g-col-md-6"),
                css_class="grid",
                style="grid-row-gap:0;",
            )
        )


class ApplicationForm(EntangledModelFormMixin, DisabledMixin, forms.ModelForm):
    ballot_name = forms.CharField(
        label="Nome na urna",
        help_text="Nome público, registrado no TSE.",
        widget=forms.TextInput(
            attrs={"placeholder": "Digite o nome que aparecerá na urna"}
        ),
    )
    number_id = forms.IntegerField(
        label="Número na urna",
        min_value=1,
        help_text="Número da candidatura",
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
        title = "Dados de candidatura"
        description = "Preencha os detalhes sobre sua candidatura."
        model = CandidatureFlow
        entangled_fields = {
            "properties": [
                "ballot_name",
                "number_id",
                "intended_position",
                "state",
                "city",
                "is_collective_mandate",
                "political_party",
                "deputy_mayor",
                "deputy_mayor_political_party",
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
                Div(Field("ballot_name"), css_class="g-col-12 g-col-md-6"),
                Div(Field("number_id"), css_class="g-col-12 g-col-md-6"),
                Div(Field("intended_position"), css_class="g-col-12 g-col-md-6"),
                Div(Field("political_party"), css_class="g-col-12 g-col-md-6"),
                Div(Field("state"), css_class="g-col-12 g-col-md-6"),
                Div(Field("city"), css_class="g-col-12 g-col-md-6"),
                Div(
                    NoCrispyField("is_collective_mandate"),
                    css_class="g-col-12 g-col-md-6 mb-3",
                ),
                Div(
                    HTML(
                        """
                        <hr/>
                        <h5 class="fw-bold">Informações sobre vice-prefeitura</h5>
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
    "Descreva brevemente sua proposta. Até 600 caracteres."
)


class ProposeForm(EntangledModelFormMixin, DisabledMixin, forms.ModelForm):
    transporte_e_mobilidade = CheckboxTextField(
        checkbox_label="Transporte e mobilidade",
        help_text="Transporte coletivo gratuito e de qualidade, modais com menos emissões e mobilidade ativa.",
        text_label=propose_text_label,
        text_help_text=propose_text_help_text,
        required=False,
        max_length=600
    )
    gestao_de_residuos = CheckboxTextField(
        checkbox_label="Gestão de resíduos",
        help_text="Compostagem de resíduos orgânicos, economia circular, mais iniciativas de catadores e catadoras de materiais recicláveis, uso de materiais biodegradáveis.",
        text_label=propose_text_label,
        text_help_text=propose_text_help_text,
        required=False,
        max_length=600

    )
    povos_originarios_tradicionais = CheckboxTextField(
        checkbox_label="Povos e comunidades tradicionais",
        help_text="Direitos, reconhecimento e valorização de conhecimentos e tecnologias de povos e comunidades tradicionais.",
        text_label=propose_text_label,
        text_help_text=propose_text_help_text,
        required=False,
        max_length=600

    )
    educacao_climatica = CheckboxTextField(
        checkbox_label="Educação climática",
        help_text="Ensino sobre meio ambiente e mudanças climáticas nas escolas, formação profissional para empregos verdes, formação de agentes populares para gestão do risco climático.",
        text_label=propose_text_label,
        text_help_text=propose_text_help_text,
        required=False,
        max_length=600

    )
    combate_racismo_ambiental = CheckboxTextField(
        checkbox_label="Enfrentamento ao racismo ambiental",
        help_text="Cultura viva, segurança cidadã, participação ativa das comunidades, protagonismo de pessoas negras, indígenas e jovens na construção de soluções.",
        text_label=propose_text_label,
        text_help_text=propose_text_help_text,
        required=False,
        max_length=600

    )
    moradia_digna = CheckboxTextField(
        checkbox_label="Moradia digna",
        help_text="Políticas habitacionais justas e participativas, moradia resiliente aos impactos de eventos climáticos extremos, eficiência hídrica e energética.",
        text_label=propose_text_label,
        text_help_text=propose_text_help_text,
        required=False,
        max_length=600

    )
    transicao_energetica = CheckboxTextField(
        checkbox_label="Transição energética justa",
        help_text="Mais fontes de energias renováveis que substituam gradualmente o uso de fontes poluidoras e garantam os direitos socioambientais das populações em seus territórios.",
        text_label=propose_text_label,
        text_help_text=propose_text_help_text,
        required=False,
        max_length=600

    )
    agricultura_sustentavel = CheckboxTextField(
        checkbox_label="Alimentos saudáveis",
        help_text="Agricultura livre de agrotóxicos, produção agroecológica, agricultura familiar e mais vegetais na mesa da população.",
        text_label=propose_text_label,
        text_help_text=propose_text_help_text,
        required=False,
        max_length=600

    )
    direito_a_cidade = CheckboxTextField(
        checkbox_label="Direito à cidade",
        help_text="Mais áreas verdes e parques públicos, menos ilhas de calor, segurança pública e bem-estar urbano, cidades mais sustentáveis e inclusivas.",
        text_label=propose_text_label,
        text_help_text=propose_text_help_text,
        required=False,
        max_length=600

    )
    adaptacao_reducao_desastres = CheckboxTextField(
        checkbox_label="Adaptação e redução de desastres",
        help_text="Políticas públicas para pessoas atingidas por eventos climáticos extremos, projetos e recursos para infraestrutura resiliente, monitoramento e resposta rápida a desastres ambientais.",
        text_label=propose_text_label,
        text_help_text=propose_text_help_text,
        required=False,
        max_length=600

    )
    direito_dos_animais = CheckboxTextField(
        checkbox_label="Proteção de animais",
        help_text="Habitats da fauna local protegidos, controle de zoonoses para evitar doenças vetoriais agravadas pela crise climática.",
        text_label=propose_text_label,
        text_help_text=propose_text_help_text,
        required=False,
        max_length=600

    )
    economia_verde = CheckboxTextField(
        checkbox_label="Economia Verde",
        help_text="Indústrias e processos produtivos sem carbono, bioeconomia, novos empregos verdes.",
        text_label=propose_text_label,
        text_help_text=propose_text_help_text,
        required=False,
        max_length=600

    )
    pessoas_afetadas_desastres = CheckboxTextField(
        checkbox_label="Pessoas afetadas por desastres",
        help_text="Políticas públicas de recuperação ambiental e assistência imediata, incluindo moradias sustentáveis e serviços de saúde física e mental, para comunidades impactadas por desastres ambientais.",
        text_label=propose_text_label,
        text_help_text=propose_text_help_text,
        required=False,
        max_length=600

    )
    

    class Meta:
        title = "Suas propostas"
        model = CandidatureFlow
        entangled_fields = {
            "properties": [
                "transporte_e_mobilidade",
                "gestao_de_residuos",
                "povos_originarios_tradicionais",
                "educacao_climatica",
                "combate_racismo_ambiental",
                "moradia_digna",
                "transicao_energetica",
                "agricultura_sustentavel",
                "direito_a_cidade",
                "adaptacao_reducao_desastres",
                "direito_dos_animais",
                "economia_verde",
                "pessoas_afetadas_desastres"
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
        help_text="Fale um pouco sobre você e sua jornada até aqui. Até 500 caracteres.",
        max_length=500
    )
    milestones = InlineArrayField(
        forms.CharField(max_length=140, required=False),
        required=False,
        label="Histórico de atuação",
        item_label="Realização",
        add_button_text="Adicionar outra",
        help_text="Adicione momentos e realizações marcantes da sua trajetória. Até 150 caracteres.",
        placeholder="Recebi o Prêmio XYZ pela Iniciativa Ambiental",
    )

    def clean_milestones(self):
        value = self.cleaned_data["milestones"]
        return value

    class Meta:
        title = "Trajetória"
        description = "Compartilhe um pouco sobre sua trajetória. Essas informações ajudarão os eleitores a conhecerem melhor sua história e seu compromisso com a causa."
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
                Div(
                    HTML("""<hr class="mb-4"/>"""),
                    css_class="g-col-12 g-col-md-12",
                ),
                Div(Field("milestones"), css_class="g-col-12"),
                css_class="grid",
                style="grid-row-gap:0;",
            )
        )


class ProfileForm(EntangledModelFormMixin, DisabledMixin, forms.ModelForm):
    video = VideoField(label="Vídeo", required=False, help_text="Tamanho máximo 50mb.")
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
        add_button_text="Adicionar outra",
        help_text="Conecte suas redes sociais para ampliar sua visibilidade e engajamento com os eleitores.",
    )

    def clean_social_media(self):
        value = self.cleaned_data["social_media"]
        return value

    class Meta:
        title = "Complemente seu perfil"
        description = "Adicione mais detalhes ao seu perfil para torná-lo completo e atrativo aos eleitores. Essas informações ajudarão a construir uma apresentação mais detalhada e engajadora."
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
                Div(
                    HTML("""<hr class="mb-4"/>"""),
                    css_class="g-col-12 g-col-md-12",
                ),
                Div(Field("social_media"), css_class="g-col-12"),
                css_class="grid",
                style="grid-row-gap:0;",
            )
        )


class CheckoutForm(EntangledModelFormMixin, DisabledMixin, forms.ModelForm):
    is_valid = HTMLBooleanField(
        label=f'Ao preencher o formulário e se cadastrar na Campanha, você está ciente de que seus dados pessoais serão tratados de acordo com o <a href="{static("docs/aviso-de-privacidade-candidaturas.pdf")}" target="_blank">Aviso de Privacidade</a>.'
    )

    class Meta:
        title = "Confirmar informações"
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