from django.conf import settings

from cms.plugin_pool import plugin_pool

from nossas.design.cms_plugins import UICMSPluginBase

from nossas.plugins.models.containermodel import Container
from nossas.plugins.forms.containerform import ContainerPluginForm


@plugin_pool.register_plugin
class ContainerPlugin(UICMSPluginBase):
    name = "Container"
    module = "NOSSAS"
    model = Container
    form = ContainerPluginForm
    render_template = "nossas/plugins/container.html"
    allow_children = True
    child_classes = settings.NOSSAS_CONTENT_PLUGINS or []
    fieldsets = (
        (None, {"fields": ["attributes", "background", "fluid"]}),
        (
            "Espaçamento",
            {
                "fields": [("padding")],
                "classes": ["collapse"],
            },
        ),
        (
            "Borda",
            {
                "fields": [
                    ("border_start", "border_top", "border_end", "border_bottom")
                ],
                "classes": ["collapse"],
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if not change and len(obj.attributes.get("padding", [])) == 0:
            obj.attributes.update({"padding": [{"side": "y", "spacing": "4"}]})

        return super().save_model(request, obj, form, change)
