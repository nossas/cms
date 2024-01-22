from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from cms.api import add_plugin
from djangocms_text_ckeditor.utils import plugin_to_tag
from cms.models.fields import PlaceholderField
from cms.models.pluginmodel import CMSPlugin
from filer.fields.image import FilerImageField
from translated_fields import TranslatedField
from tag_fields.managers import ModelTagsManager

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
    opened = "opened", "Aberta"
    done = "done", "Concluída"


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
                # "link_context": "amarelo-nossas",
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


class CampaignListPluginModel(CMSPlugin):
    def copy_relations(self, old_instance):
        self.queries.all().delete()

        for query_obj in old_instance.queries.all():
            # instance.pk = None; instance.pk.save() is the slightly odd but
            # standard Django way of copying a saved model instance
            query_obj.pk = None
            query_obj.plugin = self
            query_obj.save()


class QueryAttributes(models.TextChoices):
    status = "status", "Status"


class QueryCampaignList(models.Model):
    attribute_name = models.CharField(max_length=20, choices=QueryAttributes.choices)
    value = models.CharField(max_length=255, null=True, blank=True)

    plugin = models.ForeignKey(
        CampaignListPluginModel, related_name="queries", on_delete=models.CASCADE
    )

    def get_qs_filter(self):
        return {self.attribute_name: self.value}
