from django.db import models

from org_nossas.nossas.design.models import UIBackgroundMixin, NamingPluginMixin, UICMSPlugin


class Box(UIBackgroundMixin, NamingPluginMixin, UICMSPlugin):
    def get_classes(self):
        classes = super().get_classes()

        color = self.attributes.get("color", "").replace("bg-", "text-")

        return classes + [color]
