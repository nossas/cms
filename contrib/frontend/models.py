from django.db import models

from cms.plugin_base import CMSPlugin
from filer.fields.image import FilerImageField
from colorfield.fields import ColorField

from .models_styled import BlockElementStyled, STYLED_COLOR_PALLETE


class BorderSizeChoices(models.TextChoices):
    border = "border", "Padrão (1px)"
    border_0 = "border-0", "Sem borda (0px)"
    border_2 = "border-2", "Pequeno (2px)"
    border_4 = "border-4", "Médio (4px)"
    border_8 = "border-8", "Grande (8px)"


class RoundedChoices(models.TextChoices):
    none = "rounded-none", "Sem arredondamento"
    sm = "rounded-sm", "Small"
    md = "rounded-md", "Medium"
    lg = "rounded-lg", "Large"
    xl = "rounded-xl", "Extra Large"


class Button(BlockElementStyled, CMSPlugin):
    title = models.CharField("Título", max_length=80)
    action_url = models.CharField(
        "endereço da ação", max_length=200, help_text="slug do bloco usado na URL"
    )
    target_blank = models.BooleanField(verbose_name="Abrir em nova aba?", default=False)
    bold = models.BooleanField(verbose_name="Negrito?", default=False)
    border_color = ColorField(
        verbose_name="Cor da borda",
        samples=STYLED_COLOR_PALLETE,
        format="hexa",
        blank=True,
        null=True,
    )
    border_size = models.CharField(
        verbose_name="Tamanho da borda",
        choices=BorderSizeChoices.choices,
        max_length=30,
        blank=True,
        null=True,
    )
    rounded = models.CharField(
        verbose_name="Arredondamento",
        choices=RoundedChoices.choices,
        max_length=30,
        blank=True,
        null=True,
    )

    def styles(self):
        styles = super(Button, self).styles()

        if self.background_color and not self.border_color:
            styles += f"border-color:{self.background_color};"

        return styles


class KindChoices(models.TextChoices):
    twitter = "twitter", "Twitter"
    facebook = "facebook", "Facebook"
    instagram = "instagram", "Instagram"
    site = "site", "Site"


class SocialMedia(CMSPlugin):
    def copy_relations(self, oldinstance):
        self.socialmediaitem_set.all().delete()

        for item in oldinstance.socialmediaitem_set.all():
            item.pk = None
            item.plugin = self
            item.save()


class SocialMediaItem(models.Model):
    url = models.CharField(
        verbose_name="URL",
        max_length=100,
        help_text="Insira a URL com https://",
    )
    kind = models.CharField(
        verbose_name="Tipo",
        max_length=100,
        choices=KindChoices.choices,
    )
    icon = FilerImageField(
        verbose_name="Ícone", blank=True, null=True, on_delete=models.SET_NULL
    )
    plugin = models.ForeignKey(SocialMedia, on_delete=models.CASCADE)


class Partners(CMSPlugin):
    def copy_relations(self, oldinstance):
        self.partnersitem_set.all().delete()

        for item in oldinstance.partnersitem_set.all():
            item.pk = None
            item.plugin = self
            item.save()


class PartnersItem(models.Model):
    url = models.CharField(
        verbose_name="URL",
        max_length=100,
        blank=True,
        null=True,
        help_text="Insira a URL com https://",
    )
    icon = FilerImageField(
        verbose_name="Logo",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    plugin = models.ForeignKey(Partners, on_delete=models.CASCADE)
