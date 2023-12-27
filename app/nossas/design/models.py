from django.db import models

from cms.models.pluginmodel import CMSPlugin


class UIProperties(CMSPlugin):
    attributes = models.JSONField(null=True, blank=True)

    class Meta:
        abstract = True

    # def add_class(self, values=[]):
    #     self._classes.extend(values)
    

    @property
    def classes(self):
        return " ".join(self.attributes.values())
