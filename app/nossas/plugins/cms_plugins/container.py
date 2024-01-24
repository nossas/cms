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
    fieldsets = (
        (None, {"fields": ["attributes"]}),
        ("Fundo", {"fields": ["background"]}),
        ("Espaçamento", {"fields": [("padding")]}),
        (
            "Borda",
            {"fields": [("border_start", "border_top", "border_end", "border_bottom")]},
        ),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            self.fieldsets = (
                ("Fundo", {"fields": ["background"]}),
                ("Espaçamento", {"fields": [("padding")]}),
                (
                    "Borda",
                    {
                        "fields": [
                            (
                                "border_start",
                                "border_top",
                                "border_end",
                                "border_bottom",
                            )
                        ]
                    },
                ),
            )

        return super().get_fieldsets(request, obj)
