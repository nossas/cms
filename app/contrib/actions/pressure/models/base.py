from typing import Any
from django.db import models

from contrib.actions.fields import CampaignField

from .targets import Target


class Pressure(models.Model):
    targets = models.ManyToManyField(Target, verbose_name="Alvos", blank=True)
    campaign = CampaignField(verbose_name="Campanha", blank=True, null=True)

    class Meta:
        verbose_name = "pressão"
        verbose_name_plural = "pressões"

    def __str__(self):
        if self.campaign:
            return self.campaign.name
        return self.__str__()


class PressureAbstractModel(models.Model):
    plugin = models.ForeignKey(Pressure, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class EmailPressure(PressureAbstractModel):
    reply_to = models.CharField(verbose_name="E-mail para resposta", max_length=120)
    subject = models.CharField(verbose_name="Assunto do e-mail", max_length=120)
    body = models.TextField(verbose_name="Corpo do e-mail")

    class Meta:
        verbose_name = "email"


class PhonePressure(PressureAbstractModel):
    guide = models.TextField(verbose_name="Roteiro da ligação")

    class Meta:
        verbose_name = "telefone"


class TwitterPressure(PressureAbstractModel):
    message = models.TextField(verbose_name="Tweet")

    class Meta:
        verbose_name = "twitter"
