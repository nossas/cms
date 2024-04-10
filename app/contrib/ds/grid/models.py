from django.db import models
from cms.models import CMSPlugin


class Grid(CMSPlugin):
    gap = models.IntegerField(default=1, help_text="Unidade de medida em 'rem'")


class Column(CMSPlugin):
    span = models.IntegerField(default=6)
    span_mobile = models.IntegerField(default=12)

    def __str__(self):
        return f'({self.span}/{self.span_mobile} colunas)'