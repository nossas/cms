from django.db import models
from django.utils.functional import lazy
from django.urls import reverse

from .csv.choices import get_states


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
    indigenous = "indigena", "Indigena"
    pardo = "parda", "Parda"
    no_answer = "não declarada", "Não declarada"


class Address(models.Model):
    state = models.CharField("Estado", max_length=2, choices=lazy(get_states, list)())
    city = models.CharField("Cidade", max_length=80)
    neighborhood = models.CharField("Bairro onde se candidatou", max_length=80)

    def __str__(self):
        return f"{self.neighborhood}, {self.city} - {self.state}"


class PollingPlace(models.Model):
    name = models.CharField("Nome", max_length=120)
    address_line = models.CharField("Endereço", max_length=200, null=True, blank=True)
    places = models.ManyToManyField(Address)

    def __str__(self):
        return self.name
        # return f"{list(map(lambda x: x, self.places.all()))}".replace('[<Address:', '').replace('>]', ' ')


class CandidateStatusChoices(models.TextChoices):
    published = "published", "Publicado"
    disabled = "disabled", "Desabilitado"


class Candidate(models.Model):
    BOOL_CHOICES = ((True, "Sim"), (False, "Não"))

    slug = models.SlugField("Seu link personalizado", max_length=120, unique=True)
    name = models.CharField("Nome", max_length=120)
    bio = models.TextField("Minibio")
    email = models.EmailField("Email")
    birth = models.DateField("Data de nascimento")
    occupation = models.CharField("Profissão", max_length=100)
    photo = models.FileField(
        "Foto", null=True, blank=True, upload_to="candidaturas/fotos/"
    )
    video = models.FileField(
        "Video", null=True, blank=True, upload_to="candidaturas/videos/"
    )
    gender = models.CharField("Gênero", choices=GenderChoices.choices, max_length=20)
    is_trans = models.BooleanField(
        "Se identifica como pessoa transgênero/transexual?",
        default=False,
        choices=BOOL_CHOICES,
    )
    race = models.CharField("Raça", choices=RaceChoices.choices, max_length=20)
    social_media = models.JSONField("Rede social", null=True, blank=True)
    number = models.PositiveSmallIntegerField("Numero de voto")
    is_reelection = models.BooleanField(
        "Está se candidatando para reeleição?", default=False, choices=BOOL_CHOICES
    )
    newsletter = models.BooleanField(
        "Quero receber atualizações da campanha e do NOSSAS.", default=False
    )
    status = models.CharField(
        "Status",
        max_length=20,
        choices=CandidateStatusChoices.choices,
        default=CandidateStatusChoices.published,
    )

    place = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("eleicao:candidate_detail", kwargs={"slug": self.slug})

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
    name = models.CharField("Nome", max_length=120)
    email = models.EmailField("Email")
    whatsapp = models.CharField("Whatsapp", max_length=15, null=True, blank=True)

    zone = models.ForeignKey(PollingPlace, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return f"/querovotar/resultado/?zone={self.zone.id}"
