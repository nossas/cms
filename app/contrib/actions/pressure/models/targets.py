from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager


class CustomCurrentSiteManager(CurrentSiteManager):
    """TODO: This class created to fix sites field_name"""

    def _get_field_name(self):
        return "publish_on"

    def get_queryset(self):
        return super().get_queryset().filter(**{"publish_on__id": settings.SITE_ID})
    
    def all(self):
        return self.get_queryset()

class Target(models.Model):
    name = models.CharField(verbose_name="Nome do alvo", max_length=155)
    note = models.TextField(verbose_name="Anotações", blank=True, null=True)
    publish_on = models.ForeignKey(Site, on_delete=models.CASCADE)

    on_site = CustomCurrentSiteManager("publish_on")

    class Meta:
        verbose_name = "alvo"

    def __str__(self):
        return self.name


class ContactKindChoices(models.TextChoices):
    email_address = "email_address", "Endereço de e-mail"
    phone_number = "phone_number", "Número de telefone"
    twitter = "twitter", "Twitter"
    invalid = "invalid", "Outra opção"


class Contact(models.Model):
    kind = models.CharField(
        verbose_name="Tipo do contato",
        choices=ContactKindChoices.choices,
        max_length=20,
    )
    name = models.CharField(
        verbose_name="Nome do contato",
        help_text="Ex. Gabinete 01",
        max_length=100,
        blank=True,
        null=True,
    )
    # Valor precisa ser alterado de acordo com o tipo
    value = models.CharField(verbose_name="Valor", max_length=100)

    people = models.ForeignKey(Target, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "contato"
        unique_together = ("kind", "value")
