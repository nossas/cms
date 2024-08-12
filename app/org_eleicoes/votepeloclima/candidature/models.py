from django.db import models
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.text import slugify


# Acompanhar validação da candidatura
# Armazenar e acompanhar etapas do preenchimento das informações


class Candidature(models.Model):
    # Step 1
    legal_name = models.CharField(max_length=150)
    ballot_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    email = models.EmailField()
    cpf_cnpj = models.CharField(max_length=30)
    tse_id = models.CharField(max_length=30, null=True, blank=True)
    # Step 2
    number_id = models.PositiveIntegerField()
    intended_position = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    city = models.CharField(max_length=60)
    is_collective_mandate = models.BooleanField(default=False, blank=True)
    political_party = models.CharField(max_length=60)
    # Step 3
    video = models.FileField(upload_to="candidatures/videos/", null=True, blank=True)
    photo = models.FileField(upload_to="candidatures/photos/", null=True, blank=True)
    gender = models.CharField(max_length=30)
    color = models.CharField(max_length=30)
    sexuality = models.CharField(max_length=30, null=True, blank=True)
    social_media = models.JSONField(blank=True, null=True, default=list)
    # Step 4
    education = models.CharField(max_length=50, null=True, blank=True)
    employment = models.CharField(max_length=50, null=True, blank=True)
    short_description = models.TextField()
    milestones = models.JSONField(blank=True, null=True, default=list)
    # Step 5
    flags = models.JSONField(blank=True)
    # Step 6
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
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f"{slugify(self.ballot_name)}-{self.number_id}"
        super().save(*args, **kwargs)


class CandidatureFlowStatus(models.TextChoices):
    draft = "draft", "Editando"
    submitted = "submitted", "Enviado"
    invalid = "invalid", "Inválido"
    is_valid = "is_valid", "Válido"
    draft_requested = "draft_requested", "Edição Requisitada"


class CandidatureFlow(models.Model):
    # Propriedades só podem ser editadas quando status for `draft`
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