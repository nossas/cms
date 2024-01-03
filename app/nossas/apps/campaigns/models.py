from django.db import models

from cms.models.pluginmodel import CMSPlugin
from filer.fields.image import FilerImageField
from translated_fields import TranslatedField

from nossas.apps.basemodel import OnSiteBaseModel


class CampaignStatus(models.TextChoices):
    opened = "opened", "Aberta"
    closed = "closed", "Fechada"
    done = "done", "Concluída"


class Campaign(OnSiteBaseModel):
    name = models.CharField(max_length=180)
    description = TranslatedField(models.TextField(), {"en": {"blank": True}})
    picture = FilerImageField(on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=6, choices=CampaignStatus.choices)

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
