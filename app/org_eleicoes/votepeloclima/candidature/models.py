from django.db import models
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder

from .choices import CandidatureFlowStatus


# Acompanhar validação da candidatura
# Armazenar e acompanhar etapas do preenchimento das informações


class Candidature(models.Model):
    legal_name = models.CharField(max_length=150)
    ballot_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    email = models.EmailField()
    cpf = models.CharField(max_length=30)
    number_id = models.PositiveIntegerField()
    intended_position = models.CharField(max_length=50)
    state = models.CharField(max_length=10)
    city = models.CharField(max_length=60)
    is_collective_mandate = models.BooleanField(default=False, blank=True)
    political_party = models.CharField(max_length=60)
    video = models.FileField(upload_to="candidatures/videos/", null=True, blank=True)
    photo = models.FileField(upload_to="candidatures/photos/", null=True, blank=True)
    gender = models.CharField(max_length=30)
    color = models.CharField(max_length=30)
    sexuality = models.CharField(max_length=30, null=True, blank=True)
    social_media = models.JSONField(blank=True, null=True, default=list)
    education = models.CharField(max_length=50, null=True, blank=True)
    employment = models.CharField(max_length=50, null=True, blank=True)
    short_description = models.TextField()
    milestones = models.JSONField(blank=True, null=True, default=list)
    flags = models.JSONField(blank=True)
    appointments = models.JSONField(blank=True)

    class Meta:
        verbose_name = "Candidatura"

    @property
    def status(self):
        if self.candidatureflow:
            return self.candidatureflow.get_status_display

        return CandidatureFlowStatus.draft


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