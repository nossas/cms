from django.db import models
from django.utils.translation import gettext_lazy as _

from cms.models import CMSPlugin, Page
from contrib.ds.bs_icons import ICONS_CHOICES


class Context(models.TextChoices):
    primary = "primary"
    secondary = "secondary"
    success = "success"
    danger = "danger"
    warning = "warning"
    info = "info"
    light = "light"
    dark = "dark"
    link = "link"


class Target(models.TextChoices):
    _self = "_self", _("Abrir na mesma aba")
    _blank = "_blank", _("Abrir em nova aba")


class Styled(models.TextChoices):
    default = "", _("Padrão")
    outline = "outline", _("Contorno")
    inverted = "inverted", _("Invertido")


class Size(models.TextChoices):
    small = "sm", _("Pequeno")
    default = "", _("Médio")
    large = "lg", _("Grande")


class IconPosition(models.TextChoices):
    left = "left", _("Esquerda")
    right = "right", _("Direita")


class Button(CMSPlugin):
    label = models.CharField(max_length=100)
    link_target = models.CharField(
        verbose_name=_("Comportamento do link"),
        help_text=_("Escolha como o link será aberto ao ser clicado"),
        max_length=7,
        choices=Target.choices,
        default=Target._self,
    )
    context = models.CharField(
        verbose_name=_("Aparência"),
        max_length=30,
        choices=Context.choices,
        default=Context.primary,
    )
    styled = models.CharField(
        verbose_name=_("Estilo"),
        max_length=30,
        choices=Styled.choices,
        null=True,
        blank=True,
    )
    size = models.CharField(
        verbose_name=_("Tamanho"),
        max_length=30,
        choices=Size.choices,
        default=Size.default,
        null=True,
        blank=True,
    )
    external_link = models.CharField(
        verbose_name=_("Link externo"),
        null=True,
        blank=True,
        max_length=2040,
        # validators=url_validators,
        # help_text=_('Forneça um link para uma fonte externa.'),
    )
    internal_link = models.ForeignKey(
        Page,
        verbose_name=_("Link interno"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        # help_text=_('Se fornecido, substitui o link externo.'),
    )

    icon = models.CharField(
        verbose_name=_("Ícone"),
        max_length=30,
        choices=ICONS_CHOICES,
        blank=True,
        null=True,
    )
    icon_position = models.CharField(
        verbose_name=_("Posição do ícone"),
        max_length=10,
        choices=IconPosition.choices,
        default=IconPosition.left
    )

    @property
    def url(self):
        if self.internal_link:
            return self.internal_link.get_absolute_url()
        elif self.external_link:
            return self.external_link

        return None
