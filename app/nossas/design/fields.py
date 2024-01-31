from django import forms
from django.db import models


class GraphicElementRadioSelect(forms.RadioSelect):
    template_name = "design/fields/graphic_element_select.html"
    option_template_name = "design/fields/graphic_element_select_option.html"

    class Media:
        css = {"all": ("djangocms_frontend/css/button_group.css",)}


class GraphicElementChoices(models.TextChoices):
    questionador = "questionador", "Questionador"
    hub = "hub", "Hub, Eixo"
    impacto = "impacto", "Impacto"
    empatico = "empatico", "Empático"