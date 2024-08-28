from django.db import models
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.text import slugify
from django.utils.html import mark_safe

from .choices import CandidatureFlowStatus, IntendedPosition, PoliticalParty, Gender, Color, Sexuality, Education
from .locations_utils import get_choices, get_states


# Acompanhar validação da candidatura
# Armazenar e acompanhar etapas do preenchimento das informações


class Candidature(models.Model):
    legal_name = models.CharField(verbose_name="Nome", max_length=150)
    ballot_name = models.CharField(verbose_name="Nome na urna", max_length=100)
    birth_date = models.DateField(verbose_name="Data de nascimento")
    email = models.EmailField()
    cpf = models.CharField(max_length=30)
    number_id = models.PositiveIntegerField()
    intended_position = models.CharField(verbose_name="Tipo de candidatura", max_length=50, choices=IntendedPosition.choices)
    deputy_mayor = models.CharField(max_length=140, blank=True, null=True)
    deputy_mayor_political_party = models.CharField(max_length=60, blank=True, null=True)
    state = models.CharField(verbose_name="Estado", max_length=10)
    city = models.CharField(verbose_name="Município", max_length=60)
    is_collective_mandate = models.BooleanField(verbose_name="Tipo de mandato", default=False, blank=True)
    political_party = models.CharField(verbose_name="Partido político", max_length=60, choices=PoliticalParty.choices)
    video = models.FileField(upload_to="candidatures/videos/", null=True, blank=True)
    photo = models.FileField(upload_to="candidatures/photos/", null=True, blank=True)
    gender = models.CharField(max_length=30)
    color = models.CharField(max_length=30)
    sexuality = models.CharField(max_length=30, null=True, blank=True, choices=Sexuality.choices)
    social_media = models.JSONField(blank=True, null=True, default=list)
    education = models.CharField(max_length=50, null=True, blank=True, choices=Education.choices)
    employment = models.CharField(max_length=50, null=True, blank=True)
    short_description = models.TextField()
    milestones = models.JSONField(blank=True, null=True, default=list)
    proposes = models.JSONField(blank=True)
    appointments = models.JSONField(blank=True)

    # friendly url by ballot_name
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)

    class Meta:
        verbose_name = "Candidatura"

    @property
    def status(self):
        if self.candidatureflow:
            return self.candidatureflow.get_status_display

        return CandidatureFlowStatus.draft
    
    @property
    def get_state_display(self):
        states = dict(get_states())
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
    def get_proposes_display(self):
        from org_eleicoes.votepeloclima.candidature.forms import ProposeForm

        form = ProposeForm()
        proposes = []
        for field_name, value in self.proposes.items():
            if value:
                proposes.append(form[field_name].checkbox_label)

        return proposes

    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f"{slugify(self.ballot_name)}-{self.number_id}"
        super().save(*args, **kwargs)


class CandidatureFlow(models.Model):
    # Propriedades só podem ser editadas quando status for `draft`
    photo = models.ImageField(upload_to="candidatures/photos/", null=True)
    video = models.FileField(upload_to="candidatures/videos/", null=True, blank=True)

    properties = models.JSONField(blank=True, encoder=DjangoJSONEncoder, default=dict)
    status = models.CharField(
        max_length=50,
        choices=CandidatureFlowStatus.choices,
        default=CandidatureFlowStatus.draft,
    )

    # Registro das etapas de validação
    # Quem validou? Manual, Bot
    # Quando foi validado? Data da ação
    # Validado ou não
    # Comentário sobre
    validations = models.JSONField(blank=True, null=True)

    # Etapa 2
    # - Preenchimento da Candidatura
    # - Envio da Candidatura para avaliação
    # - Validadores automatizados
    # - Validatores manuais
    candidature = models.OneToOneField(
        Candidature, null=True, on_delete=models.SET_NULL
    )

    # Etapa 1
    # - Criar usuário desabilitado `is_active=False`
    # - Enviar e-mail para validar o usuário e criar uma senha de acesso
    # - Habilitar usuário `is_active=True`
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)

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