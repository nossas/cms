from django.db import models
from cms.models import CMSPlugin


class AlignmentItems(models.TextChoices):
    start = "start", "Start"
    center = "center", "Center"
    end = "end", "End"


class Grid(CMSPlugin):
    gap = models.IntegerField(default=1, help_text="Unidade de medida em 'rem'")
    alignment = models.CharField(
        max_length=6, choices=AlignmentItems.choices, null=True, blank=True
    )


class Column(CMSPlugin):
    span = models.IntegerField(default=6)
    span_mobile = models.IntegerField(default=12)
    start = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"({self.span}/{self.span_mobile} colunas)"
