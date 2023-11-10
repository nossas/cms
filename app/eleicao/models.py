from django.db import models
from django.utils.functional import lazy
from django.urls import reverse

from .csv.choices import get_states

from cms.models import CMSPlugin


class GenderChoices(models.TextChoices):
    male = "homem", "Homem"
    female = "mulher", "Mulher"
    nonbinary = "não binário", "Não binário"
    travesti = "travesti", "Travesti"
    queer = "queer", "Queer"
    no_answer = "não declarado", "Não declarado"


class SexualityChoices(models.TextChoices):
    heterossexual = "Heterossexual"
    pansexual = "Pansexual"
    assexual = "Assexual"
    bissexual = "Bissexual"
    queer = "Queer"
    gay = "Gay"
    lesbica = "Lésbica"
    no_answer = "Não declarada"


class RaceChoices(models.TextChoices):
    white = "branca", "Branca"
    black = "preta", "Preta"
    yellow = "amarela", "Amarela"
    indigenous = "indígena", "Indígena"
    pardo = "parda", "Parda"
    no_answer = "não declarada", "Não declarada"


class PollingPlace(models.Model):
    place = models.CharField("Unidade do Conselho Tutelar", max_length=120)
    state = models.CharField("Estado", max_length=2, choices=lazy(get_states, list)())
    city = models.CharField("Cidade", max_length=80)
    reference = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Local de Votação"
        verbose_name_plural = "Locais de Votação"

    def __str__(self):
        return f"{self.place} - {self.state}"


class CandidateStatusChoices(models.TextChoices):
    published = "published", "Publicado"
    disabled = "disabled", "Desabilitado"


class Candidate(models.Model):
    BOOL_CHOICES = ((True, "Sim"), (False, "Não"))

    slug = models.SlugField("Seu link personalizado", max_length=120, unique=True)
    name = models.CharField("Nome completo", max_length=120)
    bio = models.TextField("Minibio")
    email = models.EmailField("Email", unique=True)
    birth = models.DateField("Data de nascimento")
    occupation = models.CharField("Profissão", max_length=100)
    photo = models.FileField(
        "Foto",
        null=True,
        blank=True,
        upload_to="candidaturas/fotos/",
        help_text="Envie uma foto horizontal com no mínimo 700 pixels de largura, nos formatos JPEG ou PNG, para garantir a melhor qualidade visual. 📸✨",
    )
    video = models.FileField(
        "Video",
        null=True,
        blank=True,
        upload_to="candidaturas/videos/",
        help_text="Carregue um vídeo de até 30 segundos na posição horizontal, escolhendo entre os formatos MP4, AVI ou MOV. 🎥📽️",
    )
    gender = models.CharField(
        "Gênero", choices=GenderChoices.choices, max_length=30, null=True, blank=True
    )
    is_trans = models.BooleanField(
        "Se identifica como pessoa transgênero/transexual?",
        default=False,
        choices=BOOL_CHOICES,
        null=True,
        blank=True,
    )
    race = models.CharField(
        "Raça", choices=RaceChoices.choices, max_length=30, null=True, blank=True
    )
    social_media = models.JSONField("Rede social", null=True, blank=True)
    number = models.PositiveIntegerField("Numero de voto", null=True, blank=True)
    is_reelection = models.BooleanField(
        "Está se candidatando para reeleição?", default=False, choices=BOOL_CHOICES
    )
    lgpd = models.BooleanField("Aviso de Privacidade", default=False)
    status = models.CharField(
        "Status",
        max_length=30,
        choices=CandidateStatusChoices.choices,
        default=CandidateStatusChoices.published,
    )

    place = models.ForeignKey(PollingPlace, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Candidatura"
        verbose_name_plural = "Candidaturas"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("eleicao:candidate_detail", kwargs={"slug": self.slug})

    @property
    def short_name(self):
        return self.name.split(" ")[0]

    @property
    def cut_name(self):
        name = self.name.split(" ")
        name = name[0] + " " + name[-1]
        return name

    @property
    def age(self):
        from datetime import date

        today = date.today()
        return (
            today.year
            - self.birth.year
            - ((today.month, today.day) < (self.birth.month, self.birth.day))
        )


class Voter(models.Model):
    name = models.CharField("Nome completo", max_length=120)
    email = models.EmailField("Email")
    whatsapp = models.CharField("Whatsapp", max_length=15, null=True, blank=True)
    newsletter = models.BooleanField(
        "Quero receber atualizações da campanha e do NOSSAS.", default=True
    )

    state = models.CharField("Estado", max_length=2, choices=lazy(get_states, list)())
    city = models.CharField(
        "Cidade onde você vota", max_length=100, null=True, blank=True
    )

    place = models.ForeignKey(
        PollingPlace,
        verbose_name="Local de votação",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Eleitor(a)"
        verbose_name_plural = "Eleitores"


class EleicaoCandidateList(CMSPlugin):
    city = models.CharField("Cidade", max_length=120, blank=True, null=True)
    state = models.CharField("Estado", max_length=2, blank=True, null=True, choices=lazy(get_states, list)())


class EleicaoCarousel(CMSPlugin):
    title = models.CharField("Título", max_length=120)
    description = models.CharField("Descrição", max_length=120, null=True, blank=True)


class VoterFormPluginModel(CMSPlugin):
    title = models.CharField(
        "Título",
        max_length=255,
        null=True,
        blank=True,
        default="Descubra candidatas(os) para você!",
    )
    description = models.TextField("Descrição", null=True, blank=True)
    button_text = models.CharField(
        "Texto do botão",
        max_length=100,
        null=True,
        blank=True,
        default="Quero descobrir",
    )
