from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models.fields import PlaceholderField
from cms.models.pluginmodel import CMSPlugin
from filer.fields.image import FilerImageField
from translated_fields import TranslatedField
from tag_fields.managers import ModelTagsManager

from nossas.apps.basemodel import OnSiteBaseModel


class CampaignStatus(models.TextChoices):
    opened = "opened", "Aberta"
    closed = "closed", "Fechada"
    done = "done", "Concluída"


class Campaign(OnSiteBaseModel):
    name = models.CharField(_("Nome da campanha"), max_length=180)
    description = TranslatedField(
        models.TextField(_("Nome da campanha")), {"en": {"blank": True}}
    )
    picture = FilerImageField(
        verbose_name=_("Imagem"), on_delete=models.SET_NULL, blank=True, null=True
    )
    status = models.CharField(_("Status"), max_length=6, choices=CampaignStatus.choices)

    header_image = FilerImageField(
        verbose_name=_("Cabeçalho Imagem"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="campaign_header_image",
    )
    url = models.URLField(_("Link da Campanha"), null=True, blank=True)
    release_date = models.DateField(
        _("Data de lançamento da Campanha"), null=True, blank=True
    )
    hide = models.BooleanField(_("Esconder"), default=False)

    photos_placeholder = PlaceholderField("campaign_photos_placeholder")

    #
    tags = ModelTagsManager()

    def __str__(self):
        return self.name


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
