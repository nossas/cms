from django.db import models
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.text import slugify
from django.utils.html import mark_safe

from .choices import CandidatureFlowStatus, IntendedPosition, PoliticalParty, Gender, Color, Sexuality, Education, ElectionStatus
from .locations_utils import get_choices, get_ufs


# Acompanhar validação da candidatura
# Armazenar e acompanhar etapas do preenchimento das informações

class Candidature(models.Model):
    legal_name = models.CharField(max_length=150, verbose_name="Nome")
    ballot_name = models.CharField(max_length=100, verbose_name="Nome na urna")
    birth_date = models.DateField(verbose_name="Data de nascimento")
    email = models.EmailField(verbose_name="E-mail")
    cpf = models.CharField(max_length=30, verbose_name="CPF")
    number_id = models.PositiveIntegerField(verbose_name="Número na urna")
    intended_position = models.CharField(max_length=50, choices=IntendedPosition.choices, verbose_name="Cargo pretendido")
    deputy_mayor = models.CharField(max_length=140, blank=True, null=True, verbose_name="Vice-prefeito")
    deputy_mayor_political_party = models.CharField(max_length=60, blank=True, null=True, verbose_name="Partido do vice-prefeito")
    state = models.CharField(max_length=10, verbose_name="Estado")
    city = models.CharField(max_length=60, verbose_name="Cidade")
    is_collective_mandate = models.BooleanField(default=False, blank=True, verbose_name="Mandato coletivo")
    political_party = models.CharField(max_length=60, choices=PoliticalParty.choices, verbose_name="Partido político")
    video = models.FileField(upload_to="candidatures/videos/", null=True, blank=True, verbose_name="Vídeo")
    photo = models.FileField(upload_to="candidatures/photos/", null=True, blank=True, verbose_name="Foto")
    gender = models.CharField(max_length=30, verbose_name="Gênero")
    color = models.CharField(max_length=30, verbose_name="Cor ou raça")
    sexuality = models.CharField(max_length=30, null=True, blank=True, verbose_name="Sexualidade")
    social_media = models.JSONField(blank=True, null=True, default=list, verbose_name="Redes sociais")
    education = models.CharField(max_length=80, null=True, blank=True, choices=Education.choices, verbose_name="Educação")
    employment = models.CharField(max_length=150, null=True, blank=True, verbose_name="Ocupação")
    short_description = models.TextField(verbose_name="Descrição curta")
    milestones = models.JSONField(blank=True, null=True, default=list, verbose_name="Marcos")
    proposes = models.JSONField(blank=True, verbose_name="Propostas")
    appointments = models.JSONField(blank=True, verbose_name="Compromissos")

    election_year = models.PositiveIntegerField(default=2024, verbose_name="Ano da eleição")

    # friendly url by ballot_name
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)

    #
    created_at = models.DateTimeField(verbose_name="Criado em", auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(verbose_name="Atualizado em", auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = "Candidatura"
        ordering = ["-updated_at"]
        constraints = [
            models.UniqueConstraint(fields=['cpf', 'election_year'], name='unique_cpf_per_year')
        ]

    @property
    def status(self):
        if hasattr(self, "candidatureflow"):
            return self.candidatureflow.status

        return CandidatureFlowStatus.draft
    
    @property
    def get_state_display(self):
        states = dict(get_ufs())
        return states.get(self.state, "")

    @property
    def get_city_display(self):
        cities = dict(get_choices(self.state))
        return cities.get(self.city, "")

    @property
    def get_color_display(self):
        return dict(Color.choices).get(self.color)
    
    @property
    def get_gender_display(self):
        return dict(Gender.choices).get(self.gender)

    @property
    def get_sexuality_display(self):
        return dict(Sexuality.choices).get(self.sexuality)
    
    @property
    def get_proposes_display(self):
        from org_eleicoes.votepeloclima.candidature.forms.register import ProposeForm

        form = ProposeForm()
        proposes = []
        for field_name, value in self.proposes.items():
            if value:
                proposes.append(form[field_name].checkbox_label)

        return proposes

    @property
    def get_proposes_items(self):
        from org_eleicoes.votepeloclima.candidature.forms.register import ProposeForm
        proposes_list = []

        for field_name, value in self.proposes.items():
            if value:
                proposes_list.append({
                    "label": ProposeForm().fields[field_name].checkbox_label,
                    "description": value
                })

        return proposes_list

    @property
    def get_election_result(self):
        return self.election_results.first()

    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f"{slugify(self.ballot_name)}-{self.number_id}"
        super().save(*args, **kwargs)


class ElectionResult(models.Model):
    candidature = models.ForeignKey('Candidature', on_delete=models.CASCADE, related_name='election_results')
    status = models.CharField(max_length=20, choices=ElectionStatus.choices, verbose_name="Status da eleição")


class CandidatureFlow(models.Model):
    # Propriedades só podem ser editadas quando status for `draft`
    photo = models.ImageField(upload_to="candidatures/photos/", null=True, verbose_name="Foto")
    video = models.FileField(upload_to="candidatures/videos/", null=True, blank=True, verbose_name="Vídeo")

    properties = models.JSONField(blank=True, encoder=DjangoJSONEncoder, default=dict, verbose_name="Propriedades")
    status = models.CharField(
        max_length=50,
        choices=CandidatureFlowStatus.choices,
        default=CandidatureFlowStatus.draft,
        verbose_name="Status",
    )

    # Registro das etapas de validação
    # Quem validou? Manual, Bot
    # Quando foi validado? Data da ação
    # Validado ou não
    # Comentário sobre
    validations = models.JSONField(blank=True, null=True, verbose_name="Validações")

    # Etapa 2
    # - Preenchimento da Candidatura
    # - Envio da Candidatura para avaliação
    # - Validadores automatizados
    # - Validatores manuais
    candidature = models.OneToOneField(
        Candidature, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Candidatura"
    )

    # Etapa 1
    # - Criar usuário desabilitado `is_active=False`
    # - Enviar e-mail para validar o usuário e criar uma senha de acesso
    # - Habilitar usuário `is_active=True`
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL, verbose_name="Usuário")

    #
    created_at = models.DateTimeField(verbose_name="Criado em", auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(verbose_name="Atualizado em", auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = "Formulário"
    
    @property
    def invalid_reason(self):
        for reason, item in (self.validations or {}).items():
            if item.get("status") == CandidatureFlowStatus.invalid:
                message = invalid_messages_map.get(reason)
                return mark_safe(f"""<p class="fw-bold">{message.get("title")}</p><p>{message.get("content")}</p>""")

invalid_messages_map = {
    "pesquisa-tse": {
        "title": "Candidatura não encontrada no TSE",
        "content": "A plataforma é destinada a candidaturas ativas nas eleições municipais de 2024. Na validação do seu cadastro, não encontramos sua candidatura na base do TSE. Se isso não estiver correto, entre em contato pelo e-mail votepeloclima@nossas.org e podemos checar novamente."
    },
    "multa-ambiental": {
        "title": "Candidatura tem histórico de infrações ambientais",
        "content": "A plataforma é destinada a candidaturas que são comprometidas com a pauta climática. Na validação do seu cadastro, encontramos uma infração ambiental. Se isso não estiver correto, entre em contato pelo e-mail votepeloclima@nossas.org e podemos checar novamente."
    },
    "discurso-odio-minibio": {
        "title": "Discurso antidemocrático no cadastro",
        "content": "A plataforma é destinada a candidaturas que são comprometidas com a pauta climática, que também zelam pela democracia e pelos direitos fundamentais. Na validação do seu cadastro, encontramos conteúdo com discurso antidemocrático. Edite seu perfil para revisar o conteúdo e passar por uma nova validação."
    },
    "discurso-odio-propostas": {
        "title": "Discurso antidemocrático no cadastro",
        "content": "A plataforma é destinada a candidaturas que são comprometidas com a pauta climática, que também zelam pela democracia e pelos direitos fundamentais. Na validação do seu cadastro, encontramos conteúdo com discurso antidemocrático. Edite seu perfil para revisar o conteúdo e passar por uma nova validação."
    }
}