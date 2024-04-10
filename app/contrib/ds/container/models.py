from django.db import models
from cms.models import CMSPlugin


class ContainerSize(models.TextChoices):
    sm = "sm", "sm"
    md = "md", "md"
    lg = "lg", "lg"
    xl = "xl", "xl"
    xxl = "xxl", "xxl"
    fluid = "fluid", "fluid"


class Container(CMSPlugin):
    size = models.CharField(max_length=5, choices=ContainerSize.choices, null=True, blank=True)

    def __str__(self):
        return self.size