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

    def get_menu_title(self):
        return self.menu_title or self.title

    def get_background(self):
        if self.background.startswith("url"):
            return f"bg-[{self.background}] bg-no-repeat bg-cover"
        
        return f"bg-[{self.background}]"


# class Block(BlockBase):
#     pass

class ActionButton(CMSPlugin):
    title = models.CharField("título", max_length=80)
    action_url = models.CharField(
        "endereço da ação", max_length=80, help_text="slug do bloco usado na URL"
    )
    bg_color = models.CharField(
        "cor do fundo", max_length=100, default="blue", blank=True
    )

    def get_bg_color(self):
        if self.bg_color.startswith("bg-"):
            return self.bg_color
        
        return f"bg-{{self.bg_color}}-800 hover:bg-{{self.bg_color}}-900"


class RowStyles(models.TextChoices):
    flex = ("flex", "Flex")
    wrap = ("wrap", "Wrap")


class Row(CMSPlugin):
    styled = models.CharField(
        "Estilo da linha",
        max_length=20,
        choices=RowStyles.choices,
        default=RowStyles.flex
    )

    def classnames(self, attrs=None):
        if self.styled == RowStyles.flex:
            return 'flex flex-row items-center gap-8'
        elif self.styled == RowStyles.wrap:
            return 'flex flex-wrap gap-8 justify-center'

        return ''


class ColumnStyles(models.TextChoices):
    auto = ("auto", "Auto")


class Column(CMSPlugin):
    styled = models.CharField(
        "Estilho da coluna",
        max_length=20,
        choices=ColumnStyles.choices,
        default=ColumnStyles.auto
    )

    def classnames(self, attrs=None):
        if self.styled == ColumnStyles.auto:
            return 'flex-auto'
        
        return ''