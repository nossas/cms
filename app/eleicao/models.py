from django.db import models
from django.utils.functional import lazy
from django.urls import reverse

from .csv.choices import get_states

# Create your models here.


class GenderChoices(models.TextChoices):
    male = "homem", "Homem"
    female = "mulher", "Mulher"
    nonbinary = "não binário", "Não binário"
    travesti = "travesti", "Travesti"
    queer = "queer", "Queer"
    no_answer = "não declarado", "Não declarado"


class SexualityChoices(models.TextChoices):
    heterossexual = "heterossexual"
    pansexual = "pansexual"
    assexual = "assexual"
    bissexual = "bissexual"
    queer = "queer"
    gay = "gay"
    lesbica = "lesbica"
    no_answer = "não declarada"


class RaceChoices(models.TextChoices):
    white = "branca", "Branca"
    black = "preta", "Preta"
    yellow = "amarela", "Amarela"
    indigenous = "indigena", "Indigena"
    pardo = "parda", "Parda"
    no_answer = "não declarada", "Não declarada"


class Theme(models.Model):
    value = models.SlugField("Valor", max_length=50)
    label = models.CharField("Label", max_length=50)

    def __str__(self):
        return self.label


class Address(models.Model):
    state = models.CharField("Estado", max_length=2, choices=lazy(get_states, list)())
    city = models.CharField("Cidade", max_length=80)
    neighborhood = models.CharField("Bairro", max_length=80)

    def __str__(self):
        return f"{self.neighborhood}, {self.city} - {self.state}"


class PollingPlace(models.Model):
    name = models.CharField("Nome", max_length=120)
    address_line = models.CharField("Endereço", max_length=200, null=True, blank=True)
    places = models.ManyToManyField(Address)

    def __str__(self):
        return self.name
        # return f"{list(map(lambda x: x, self.places.all()))}".replace('[<Address:', '').replace('>]', ' ')


class Candidate(models.Model):
    slug = models.SlugField("Seu link personalizado", max_length=120, unique=True)
    name = models.CharField("Nome", max_length=120)
    bio = models.TextField("Minibio")
    email = models.EmailField("Email")
    birth = models.DateField("Data de nascimento")
    occupation = models.CharField("Profissão", max_length=100)
    photo = models.FileField(
        "Foto", null=True, blank=True, upload_to="candidatos/fotos/"
    )
    video = models.FileField(
        "Video", null=True, blank=True, upload_to="candidatos/videos/"
    )
    gender = models.CharField("Genero", choices=GenderChoices.choices, max_length=20)
    is_trans = models.BooleanField("Pessoa Trans?", default=False)
    sexuality = models.CharField(
        "Sexualidade", choices=SexualityChoices.choices, max_length=20
    )
    race = models.CharField("Raça", choices=RaceChoices.choices, max_length=20)
    social_media = models.JSONField("Redes sociais", null=True, blank=True)
    number = models.PositiveSmallIntegerField("Numero do candidato")
    is_reelection = models.BooleanField("Reeleição", default=False)
    newsletter = models.BooleanField(
        "Quero receber atualizações da campanha e do NOSSAS.", default=False
    )
    themes = models.ManyToManyField(Theme)
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
