from django.db import models
from django.utils.functional import lazy

from .csv.choices import get_states

# Create your models here.


class GenderChoices(models.TextChoices):
    male = "masculino"
    female = "feminino"
    nonbinary = "não binário"
    travesti = "travesti"
    queer = "queer"
    no_answer = "não declarado"


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
    white = "branca"
    black = "preta"
    yellow = "amarela"
    indigenous = "indigena"
    pardo = "parda"
    no_answer = "não declarada"


class Theme(models.Model):
    value = models.SlugField("Valor", max_length=50)
    label = models.CharField("Label", max_length=50)

    def __str__(self):
        return self.label


class Address(models.Model):
    state = models.CharField("Estado", max_length=2, choices=lazy(get_states, list)())
    city = models.CharField("Cidade", max_length=80, choices=[])
    neighborhood = models.CharField("Bairro", max_length=50,choices=[])

    def __str__(self):
            return f"{self.neighborhood}, {self.city} - {self.state}" 

class PollingPlace(models.Model):
    name = models.CharField("Nome", max_length=120)  
    address_line = models.CharField("Endereço", max_length=200)
    places = models.ManyToManyField(Address)

    def __str__(self):
        return f"{self.name}: {self.address_line} - {self.neighborhood}"


class Candidate(models.Model):
    slug = models.SlugField("Slug", max_length=120, unique=True)
    name = models.CharField("Nome", max_length=120)
    bio = models.TextField("Minibio")
    email = models.EmailField("Email")
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

    themes = models.ManyToManyField(Theme)
    zone = models.ForeignKey(PollingPlace, on_delete=models.CASCADE)
    place = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/eleicao/candidatas/{self.slug}"


class Voter(models.Model):
    name = models.CharField("Nome", max_length=120)
    email = models.EmailField("Email")
    whatsapp = models.CharField("Whatsapp", max_length=15, null=True, blank=True)

    zone = models.ForeignKey(PollingPlace, on_delete=models.CASCADE)
