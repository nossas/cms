from django.db import models

from cms.models.pluginmodel import CMSPlugin


BOOTSTRAP_CSS_PROPERTIES = [
    "background",
]

class UIProperties(CMSPlugin):
    attributes = models.JSONField(null=True, blank=True)

    class Meta:
        abstract = True

    def get_classes(self):
        return []

    @property
    def classes(self):
        return " ".join(self.get_classes())


class UIDefaultPropertiesMixin:
    def get_classes(self):
        classes = super().get_classes()

        bootstrap_classes = dict(
            filter(
                lambda pair: pair[0] in BOOTSTRAP_CSS_PROPERTIES,
                self.attributes.items(),
            )
        )

        return classes + list(bootstrap_classes.values())


class UIPaddingPropertiesMixin:
    def get_classes(self):
        classes = super().get_classes()

        padding = self.attributes.get("padding")
        if padding and len(padding) > 0:
            classes += list(map(lambda x: f"p{x['side']}-{x['spacing']}", padding))

        return classes


class UIBorderPropertiesMixin:
    def get_classes(self):
        classes = super().get_classes()
        has_border = False

        for attr in ["border_top", "border_bottom", "border_start", "border_end"]:
            if attr in self.attributes.keys() and self.attributes[attr]:
                has_border = True

            if not self.attributes.get(attr, True):
                classes.append(f"{attr.replace('_', '-')}-0")

        if has_border:
            classes = ["border", "border-2", "border-dark"] + classes

        return classes
