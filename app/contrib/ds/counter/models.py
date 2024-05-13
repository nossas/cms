from django.db import models

from cms.models import CMSPlugin


class Counter(CMSPlugin):
    start_number = models.IntegerField(verbose_name="Número de inicio", null=True, blank=True)
    end_number = models.IntegerField(verbose_name="Número de fim", null=True, blank=True)

    start_date = models.DateField(verbose_name="Data de Início", null=True, blank=True)
    end_date = models.DateField(verbose_name="Data Final", null=True, blank=True)
    
    measurement = models.CharField(verbose_name="Unidade de medida", max_length=140, null=True, blank=True)
    description = models.TextField(verbose_name="Descrição", null=True, blank=True)
    tooltip_text = models.TextField(verbose_name="Texto do Tooltip", null=True, blank=True)
