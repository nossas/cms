from django.db import models

from cms.models.pluginmodel import CMSPlugin


BOOTSTRAP_CSS_PROPERTIES = ["background", "padding_y", "padding_x"]


class UIProperties(CMSPlugin):
    attributes = models.JSONField(null=True, blank=True)

    class Meta:
        abstract = True

    def get_classes(self):
        return ""
    
    @property
    def classes(self):
        return self.get_classes()



class UIDefaultPropertiesMixin:
    def get_classes(self):
        classes = super().get_classes()

        bootstrap_classes = dict(
            filter(
                lambda pair: pair[0] in BOOTSTRAP_CSS_PROPERTIES,
                self.attributes.items(),
            )
        )

        return classes + " " + " ".join(bootstrap_classes.values())


class UIBorderPropertiesMixin:
    def get_classes(self):
        classes = super().get_classes()
        has_border = False

        for attr in ["border_top", "border_bottom", "border_start", "border_end"]:
            if not self.attributes.get(attr, True):
                has_border = True
                classes += f" {attr.replace('_', '-')}-0"
        
        if has_border:
            classes = "border border-2 border-dark" + classes

        return classes