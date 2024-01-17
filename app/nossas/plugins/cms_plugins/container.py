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
        ("Atributos", {"fields": ["attributes"]}),
        ("Fundo", {"fields": ["background"]})
    )

    def get_form(self, request, obj, change, **kwargs):
        if not change:
            self.form = ContainerPluginForm

        return super().get_form(request, obj, change, **kwargs)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            self.fieldsets = (
                (None, {"fields": ["attributes"]}),
                ("Fundo", {"fields": ["background"]}),
            )

        return super().get_fieldsets(request, obj)
