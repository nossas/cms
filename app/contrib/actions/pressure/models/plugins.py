from django.db import models

from cms.models import CMSPlugin

from .base import Pressure
# from contrib.bonde.models import Widget


class PressurePluginModel(CMSPlugin):
    """ """
    action = models.ForeignKey(Pressure, on_delete=models.CASCADE)