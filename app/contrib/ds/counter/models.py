from django.db import models

from cms.models import CMSPlugin


class Counter(CMSPlugin):
    initial_number = models.IntegerField(verbose_name="Número de inicio", null=True, blank=True)
    target_number = models.IntegerField(verbose_name="Número de fim", null=True, blank=True)

    initial_date = models.DateField(verbose_name="Data de Início", null=True, blank=True)
    target_date = models.DateField(verbose_name="Data Final", null=True, blank=True)
