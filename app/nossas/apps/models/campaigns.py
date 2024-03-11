from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from cms.api import add_plugin
from cms.plugin_base import CMSPlugin
from cms.models.fields import PlaceholderField
from djangocms_text_ckeditor.utils import plugin_to_tag
from filer.fields.image import FilerImageField
from tag_fields.managers import ModelTagsManager
from translated_fields import TranslatedField

from nossas.apps.basemodel import OnSiteBaseModel


class CampaignGroup(OnSiteBaseModel):
    name = models.CharField(_("Nome da grupo"), max_length=180)
    community_id = models.IntegerField(_("ID da Comunidade BONDE"))

    class Meta:
        unique_together = ("site", "community_id")
        verbose_name = _("Comunidade")

    def __str__(self):
        return self.name


class CampaignStatus(models.TextChoices):
    opened = "opened", _("Aberta")
    done = "done", _("Concluída")


class Campaign(OnSiteBaseModel):
    name = models.CharField(_("Nome da campanha"), max_length=180)
    description = TranslatedField(
        models.TextField(_("Descrição")), {"en": {"blank": True}}
    )
    picture = FilerImageField(
        verbose_name=_("Imagem"), on_delete=models.SET_NULL, blank=True, null=True
    )
    status = models.CharField(_("Status"), max_length=6, choices=CampaignStatus.choices)

    campaign_group = models.ForeignKey(
        CampaignGroup, verbose_name=_("Comunidade"), on_delete=models.CASCADE, null=True
    )
    mobilization_id = models.IntegerField(
        _("ID da Mobilização BONDE"), null=True, blank=True
    )

    header_image = FilerImageField(
        verbose_name=_("Cabeçalho Imagem"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="campaign_header_image",
    )
    url = models.URLField(_("Link da Campanha"), null=True, blank=True)
    release_date = models.DateField(_("Data de lançamento"), null=True, blank=True)
    hide = models.BooleanField(_("Esconder"), default=False)

    placeholder = PlaceholderField("campaign_placeholder")

    #
    tags = ModelTagsManager()

    class Meta:
        verbose_name = _("Campanha")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("campaigns:campaign-detail", kwargs={"pk": self.pk})

    def create_default_page(self):
        language = "pt-br"

        # Cria Container da primeira parte
        plugin_type = "ContainerPlugin"
        target = add_plugin(
            placeholder=self.placeholder, plugin_type=plugin_type, language="pt-br"
        )
        # Adiciona texto dentro do Container
        plugin_type = "TextPlugin"
        child_attrs = {"body": self.description}
        add_plugin(
            placeholder=self.placeholder,
            plugin_type=plugin_type,
            language=language,
            target=target,
            **child_attrs,
        )
        # Cria Container da Chamada
        plugin_type = "ContainerPlugin"
        target = add_plugin(
            placeholder=self.placeholder,
            plugin_type=plugin_type,
            language=language,
            attributes={
                "padding": [{"side": "y", "spacing": "5"}],
                "background": "bg-azul-nossas",
                "border_top": True,
                "border_bottom": True,
            },
        )
        # # Adiciona texto dentro do Container da Chamada
        plugin_type = "TextPlugin"
        child_attrs = {
            "body": f"""<h3 style="text-align: center;">Conheça a campanha {self.name}!</h3><p style="text-align: center;">Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur lorem ipsum dolor sit amet.</p>"""
        }
        text = add_plugin(
            placeholder=self.placeholder,
            plugin_type=plugin_type,
            language=language,
            target=target,
            **child_attrs,
        )

        # Adiciona link dentro do editor de texto
        plugin_type = "LinkButtonPlugin"
        child_attrs = {
            "config": {
                "link_outline": False,
                "link_context": "amarelo-nossas",
                "link_type": "btn",
                "external_link": self.url,
                "name": "SAIBA MAIS",
            }
        }
        text_child_1 = add_plugin(
            placeholder=self.placeholder,
            plugin_type=plugin_type,
            language=language,
            target=text,
            **child_attrs,
        )
        text.body = f'{text.body}<p style="text-align: center;">{plugin_to_tag(text_child_1)}</p>'
        text.save()

        # Adiciona Plugin de Navegar por campanhas
        plugin_type = "NavigateCampaignsPlugin"
        add_plugin(
            placeholder=self.placeholder, plugin_type=plugin_type, language=language
        )


class NavigateCampaigns(CMSPlugin):
    related_campaign = models.ForeignKey(
        Campaign,
        verbose_name=_("Campanha Relacionada"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    filter_tags = models.BooleanField(verbose_name=_("Filtrar por tags?"), default=True)
    filter_campaign_group = models.BooleanField(
        verbose_name=_("Filtrar por comunidade?"), default=False
    )


class OurCitiesProject(CMSPlugin):
    name = models.CharField(verbose_name=_("Nome do projeto"), max_length=100)
    picture = FilerImageField(
        verbose_name=_("Imagem"), on_delete=models.SET_NULL, blank=True, null=True
    )
    related_campaigns = models.ManyToManyField(
        Campaign, verbose_name=_("Campanhas relacionadas"), blank=True
    )
    url = models.URLField(verbose_name=_("URL do Projeto"), blank=True, null=True)
    hide_border = models.BooleanField(verbose_name=_("Remover borda"), default=False)
