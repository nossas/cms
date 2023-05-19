from django.db import models

from cms.models import CMSPlugin


class BlockBase(CMSPlugin):
    title = models.CharField("título", max_length=80, blank=True)
    slug = models.SlugField(
        verbose_name="slug",
        max_length=80,
        blank=True,
        help_text="a parte do título que é usada na URL",
    )
    menu_title = models.CharField("título do menu", max_length=50, blank=True)
    menu_hidden = models.BooleanField("esconder menu?", default=False)

    # Styles
    background = models.CharField(
        "background", max_length=200, default="white", blank=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Block(BlockBase):
    pass

class ActionButton(CMSPlugin):
    title = models.CharField("título", max_length=80)
    action_url = models.CharField(
        "endereço da ação", max_length=80, help_text="slug do bloco usado na URL"
    )
    bg_color = models.CharField(
        "cor do fundo", max_length=50, default="blue", blank=True
    )
