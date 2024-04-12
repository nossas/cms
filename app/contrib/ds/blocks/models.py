from django.db import models

from cms.models import CMSPlugin


class AlignmentItems(models.TextChoices):
    start = "start", "Start"
    center = "center", "Center"
    end = "end", "End"

class FlexWrap(models.TextChoices):
    wrap = "wrap", "wrap"
    nowrap = "nowrap", "nowrap"
    wrapreverse = "wrap-reverse", "wrap-reverse"

class FlexDirection(models.TextChoices):
    row = "row", "row"
    column = "column", "column"
    rowreverse = "row-reverse", "row-reverse"
    columnreverse = "column-reverse", "column-reverse"

class ContainerSize(models.TextChoices):
    sm = "sm", "sm"
    md = "md", "md"
    lg = "lg", "lg"
    xl = "xl", "xl"
    xxl = "xxl", "xxl"
    fluid = "fluid", "fluid"

class BlockElement(models.TextChoices):
    section = "section", "section"
    container = "container", "container"
    div = "div", "div"


class BlockLayout(models.TextChoices):
    block = "block", "block"
    grid = "grid", "grid"
    flex = "d-flex", "flex"


class BlockAbstractModel(models.Model):
    """
    Elemento HTML em bloco.

    Tipos de elementos:
        - section
        - container
        - div

    Tipos de layouts:
        - block
        - grid
        - flex
    """

    element = models.CharField(
        max_length=9, choices=BlockElement.choices, default=BlockElement.div
    )
    layout = models.CharField(
        max_length=6, choices=BlockLayout.choices, default=BlockLayout.block
    )
    attributes = models.JSONField(null=True, blank=True)

    class Meta:
        abstract = True


class Block(BlockAbstractModel, CMSPlugin):
    
    def __str__(self):
        return f"{self.element}/{self.layout}"
