from django.db import models
from django.utils.translation import gettext_lazy as _

from cms.models import CMSPlugin
from filer.fields.image import FilerImageField


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
    section = "section", _("Seção")
    div = "div", _("Conteúdo")


class BlockLayout(models.TextChoices):
    block = "block", _("Caixa")
    grid = "grid", _("Em grade")
    flex = "d-flex", _("Flexível")

class BackgroundSize(models.TextChoices):
    contain = "contain"
    cover = "cover"
    initial = "initial"


class BlockAbstractModel(models.Model):
    """
    Elemento HTML em bloco.

    Tipos de elementos:
        - section
        - div

    Tipos de layouts:
        - block
        - grid
        - flex
    """

    element = models.CharField(
        verbose_name=_("Tipo de elemento"),
        help_text=_("Escolha a estrutura do bloco"),
        max_length=9,
        choices=BlockElement.choices,
        default=BlockElement.div,
    )
    layout = models.CharField(
        verbose_name=_("Layout"),
        help_text=_("Defina como o conteúdo será disposto"),
        max_length=6,
        choices=BlockLayout.choices,
        default=BlockLayout.block,
    )
    is_container = models.BooleanField(
        verbose_name=_("Container"),
        default=False,
    )
    background_image = FilerImageField(
            verbose_name=("Imagem de fundo"),
            blank=True,
            null=True,
            on_delete=models.SET_NULL,
    )
    background_size = models.CharField(
        choices=BackgroundSize.choices,
        max_length=8,
        default=BackgroundSize.cover
    )
    attributes = models.JSONField(null=True, blank=True)

    class Meta:
        abstract = True


class Block(BlockAbstractModel, CMSPlugin):

    class Meta:
        verbose_name = _("Bloco")

    def __str__(self):
        return f"{self.element}/{self.layout}"
