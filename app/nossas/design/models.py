from django.db import models

from cms.models.pluginmodel import CMSPlugin


class UICMSPlugin(CMSPlugin):
    attributes = models.JSONField(null=True, blank=True)

    class Meta:
        abstract = True

    def get_classes(self):
        return []

    @property
    def classes(self):
        return " ".join(self.get_classes())


class UIBackgroundMixin:
    def get_classes(self):
        classes = super().get_classes()

        bootstrap_classes = dict(
            filter(
                lambda pair: pair[0] in ["background", ],
                self.attributes.items(),
            )
        )

        return classes + list(bootstrap_classes.values())


class UIPaddingMixin:
    def get_classes(self):
        classes = super().get_classes()

        padding = self.attributes.get("padding")
        if padding and len(padding) > 0:
            classes += list(map(self.format_padding, padding))

        return classes

    def format_padding(self, property):
        if (
            property["side"] == "x"
            and property["spacing"] != "0"
            and property["spacing"] != "auto"
        ):
            return f"p{property['side']}-sm-{property['spacing']} p{property['side']}-{int(property['spacing']) - 1}"

        return f"p{property['side']}-{property['spacing']}"


class UIBorderMixin:
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
