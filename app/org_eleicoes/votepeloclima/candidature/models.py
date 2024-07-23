from django.db import models
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder


# Acompanhar validação da candidatura
# Armazenar e acompanhar etapas do preenchimento das informações


class CandidatureIntendedPosition(models.TextChoices):
    prefeitura = "prefeitura", "Prefeitura"
    vice_prefeitura = "vice_prefeitura", "Vice-Prefeitura"
    vereadore = "vereadore", "Vereador(a)"


class CandidaturePoliticalParty(models.TextChoices):
    mdb = "mdb", "MDB"
    pdt = "pdt", "PDT"
    pt = "pt", "PT"
    pcdob = "pcdob", "PCdoB"
    psb = "psb", "PSB"
    psdb = "psdb", "PSDB"
    agir = "agir", "AGIR"
    mobiliza = "mobiliza", "MOBILIZA"
    cidadania = "cidadania", "CIDADANIA"
    pv = "pv", "PV"
    avante = "avante", "AVANTE"
    pstu = "pstu", "PSTU"
    pcb = "pcb", "PCB"
    prtb = "prtb", "PRTB"
    dc = "dc", "DC"
    pco = "pco", "PCO"
    pode = "pode", "PODE"
    republicanos = "republicanos", "REPUBLICANOS"
    psol = "psol", "PSOL"
    psd = "psd", "PSD"
    solidariedade = "solidariedade", "SOLIDARIEDADE"
    novo = "novo", "NOVO"
    rede = "rede", "REDE"
    pmb = "pmb", "PMB"
    up = "up", "UP"
    uniao = "uniao", "UNIÃO"
    prd = "prd", "PRD"


class CandidatureGender(models.TextChoices):
    male = "homem", "Homem"
    female = "mulher", "Mulher"
    nonbinary = "não binário", "Não binário"
    travesti = "travesti", "Travesti"
    queer = "queer", "Queer"
    no_answer = "não declarado", "Não declarado"


class CandidatureSexuality(models.TextChoices):
    heterossexual = "Heterossexual"
    pansexual = "Pansexual"
    assexual = "Assexual"
    bissexual = "Bissexual"
    queer = "Queer"
    gay = "Gay"
    lesbica = "Lésbica"
    no_answer = "Não declarada"


class CandidatureColor(models.TextChoices):
    white = "branca", "Branca"
    black = "preta", "Preta"
    yellow = "amarela", "Amarela"
    indigenous = "indígena", "Indígena"
    pardo = "parda", "Parda"
    no_answer = "não declarada", "Não declarada"


class CandidatureEducation(models.TextChoices):
    le_e_escreve = "le_e_escreve", "Lê e escreve"
    fundamental_incompleto = "fundamental_incompleto", "Ensino Fundamental Incompleto"
    fundamental_completo = "fundamental_completo", "Ensino Fundamental Completo"
    medio_incompleto = "medio_incompleto", "Ensino Médio Incompleto"
    medio_completo = "medio_completo", "Ensino Médio Completo"
    superior_incompleto = "não superior_incompleto", "Ensino Superior Incompleto"
    superior_completo = "superior_completo", "Ensino Superior Completo"


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
    intended_position = models.CharField(
        max_length=50,
        choices=CandidatureIntendedPosition.choices,
        default=CandidatureIntendedPosition.prefeitura
    )
    state = models.CharField(max_length=2)
    city = models.CharField(max_length=60)
    is_collective_mandate = models.BooleanField(default=False, blank=True)
    political_party = models.CharField(
        max_length=60,
        choices=CandidaturePoliticalParty.choices,
        default=CandidaturePoliticalParty.mdb
    )
    # Step 3
    video = models.FileField(upload_to="cadidatures/videos/", null=True, blank=True)
    photo = models.FileField(upload_to="cadidatures/photos/", null=True, blank=True)
    gender = models.CharField(
        max_length=30,
        choices=CandidatureGender.choices,
        default=CandidatureGender.male
    )
    color = models.CharField(
        max_length=30,
        choices=CandidatureColor.choices,
        default=CandidatureColor.white
    )
    sexuality = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        choices=CandidatureSexuality.choices,
        default=CandidatureSexuality.heterossexual
    )
    social_media = models.JSONField(blank=True, null=True, default=list)
    # Step 4
    education = models.CharField(
        max_length=50,
        choices=CandidatureEducation.choices,
        default=CandidatureEducation.le_e_escreve
    )
    employment = models.CharField(max_length=50, null=True, blank=True)
    short_description = models.TextField()
    milestones = models.JSONField(blank=True, null=True, default=list)
    # Step 5
    flags = models.JSONField(blank=True)
    # Step 6
    appointments = models.JSONField(blank=True)

    class Meta:
        verbose_name = "Candidatura"

    @property
    def status(self):
        if self.candidatureflow:
            return self.candidatureflow.get_status_display

        return CandidatureFlowStatus.draft


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
