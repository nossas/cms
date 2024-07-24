from django import forms
from django.core.exceptions import ValidationError

from captcha.widgets import ReCaptchaV2Checkbox

from .models import CandidaturePoliticalParty, CandidatureIntendedPosition, CandidatureGender, CandidatureSexuality, CandidatureColor, CandidatureEducation


from .fields import (
    CheckboxTextField,
    CityCepField,
    InlineArrayField,
    Select2CustomWidget,
    StateCepField,
    ValidateOnceReCaptchaField
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
    legal_name = forms.CharField(label="Nome", help_text="Nome da pessoa que possui os dados registrados no TSE.")
    ballot_name = forms.CharField(label="Nome na urna", help_text="Nome público, registrado no TSE.")
    birth_date = forms.DateField(label="Data de nascimento")
    email = forms.EmailField(label="E-mail")
    cpf_cnpj = forms.CharField(label="CPF/CNPJ", help_text="CPF é necessário para confirmar sua identidade junto ao TSE")

    class Meta:
        title = "Informações Pessoais"
        description = "Vamos lá! Essas informações são essenciais para verificar sua candidatura e garantir a segurança. Se for uma candidatura coletiva, a pessoa responsável deve ter os dados registrados no TSE."
        footer_note = "Suas informações são usadas apenas para verificação e segurança. O processo será salvo pelo seu e-mail e, no final do cadastro, você criará uma senha e um login para acessar a Área da Candidatura."


class ApplicationForm(DisabledMixin, forms.Form):
    number_id = forms.IntegerField(label="Número de identificação", help_text="Número fornecido pelo TSE", min_value=1)
    intended_position = forms.ChoiceField(
        label="Cargo pretendido",
        help_text="Selecione o cargo que você está concorrendo",
        choices=CandidatureIntendedPosition.choices,
        widget=Select2CustomWidget()
    )
    state = StateCepField(label="Estado", help_text="Estado onde você está concorrendo")
    city = CityCepField(label="Cidade", help_text="Cidade onde você está concorrendo")
    is_collective_mandate = forms.BooleanField(
        label="É um mandato coletivo?", required=False
    )
    political_party = forms.ChoiceField(
        label="Partido político",
        choices=CandidaturePoliticalParty.choices,
        widget=Select2CustomWidget()
    )

    class Meta:
        title = "Informações de candidatura"
        description = "Preencha os detalhes sobre sua candidatura."


class ProfileForm(DisabledMixin, forms.Form):
    video = forms.URLField(label="Vídeo", required=False)
    photo = forms.URLField(label="Foto", required=False)
    gender = forms.ChoiceField(
        label="Gênero",
        choices=CandidatureGender.choices,
        widget=Select2CustomWidget()
    )
    color = forms.ChoiceField(
        label="Raça",
        choices=CandidatureColor.choices,
        widget=Select2CustomWidget()
    )
    sexuality = forms.ChoiceField(
        label="Sexualidade",
        choices=CandidatureSexuality.choices,
        widget=Select2CustomWidget()
    )
    social_media = InlineArrayField(forms.URLField(required=False), label="Redes sociais", required=False)

    def clean_social_media(self):
        value = self.cleaned_data['social_media']
        return value

    class Meta:
        title = "Complemente seu Perfil"
        description = "Adicione mais detalhes ao seu perfil para torná-lo completo e atrativo aos eleitores. Essas informações ajudarão a construir uma apresentação mais detalhada e engajadora."


class TrackForm(DisabledMixin, forms.Form):
    education = forms.ChoiceField(
        label="Escolaridade",
        choices=CandidatureEducation.choices,
        widget=Select2CustomWidget()
    )
    employment = forms.CharField(label="Ocupação", required=False)
    short_description = forms.CharField(label="Minibio", help_text="Fale um pouco sobre você e sua jornada até aqui. Até 150 caracteres.", widget=forms.Textarea())
    milestones = InlineArrayField(forms.CharField(max_length=140, required=False), label="Histórico de atuação", required=False)

    def clean_milestones(self):
        value = self.cleaned_data['milestones']
        return value

    class Meta:
        title = "Sobre sua trajetória"
        description = "Compartilhe um pouco sobre sua trajetória. Essas informações ajudarão os eleitores a conhecerem melhor sua história e seu compromisso com a causa."


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
        title = "Bandeiras e propostas"
        description = "Máximo de 5 seleções. Escolha até 5 bandeiras que você defenderá e descreva suas propostas para cada uma delas. Essas informações ajudarão os eleitores a entender melhor suas prioridades e ações."
    
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
        description = "Esses são os compromissos climáticos que todos os candidatos devem assumir ao criar um perfil no Vote pelo Clima. Eles ficarão visíveis aos eleitores, mostrando seu empenho em um futuro sustentável. Vamos juntos nessa?"


class CheckoutForm(forms.Form):
    is_valid = forms.BooleanField()

    class Meta:
        title = "Para finalizar, confirme suas informações"
        description = "Revise todas as informações fornecidas. Após finalizar, você terá acesso a uma área restrita onde poderá visualizar e editar suas informações. Certifique-se de que todos os dados estão corretos para evitar solicitações de edição desnecessárias."
        footer_note = "Ao preencher o formulário e se cadastrar na Campanha, você está ciente de que seus dados pessoais serão tratados de acordo com o Aviso de Privacidade."


register_form_list = [
    ("captcha", CaptchaForm),
    ("compromissos", AppointmentForm),
    ("informacoes-pessoais", InitialForm),
    ("informacoes-de-candidatura", ApplicationForm),
    ("bandeiras-da-sua-candidatura", FlagForm),
    ("sobre-sua-trajetoria", TrackForm),
    ("complemente-seu-perfil", ProfileForm),
    ("checkout", CheckoutForm),
]
