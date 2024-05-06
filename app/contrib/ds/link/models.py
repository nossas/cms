from django.db import models

from cms.models import CMSPlugin, Page


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
    _blank = "_blank"
    _self = "_self"
    _parent = "_parent"
    _top = "_top"


class Styled(models.TextChoices):
    default = "", "Default"
    outline = "outline", "Outline"
    inverted = "inverted", "Inverted"


class Button(CMSPlugin):
    label = models.CharField(max_length=100)
    link_target = models.CharField(
        max_length=7, choices=Target.choices, null=True, blank=True
    )
    context = models.CharField(
        max_length=30, choices=Context.choices, null=True, blank=True
    )
    styled = models.CharField(
        max_length=30, choices=Styled.choices, null=True, blank=True
    )
    external_link = models.CharField(
        # verbose_name=_('Link externo'),
        null=True,
        blank=True,
        max_length=2040,
        # validators=url_validators,
        # help_text=_('Forneça um link para uma fonte externa.'),
    )
    internal_link = models.ForeignKey(
        Page,
        # verbose_name=_('Link interno'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        # help_text=_('Se fornecido, substitui o link externo.'),
    )

    @property
    def url(self):
        if self.internal_link:
            return self.internal_link.get_absolute_url()
        elif self.external_link:
            return self.external_link

        return None
