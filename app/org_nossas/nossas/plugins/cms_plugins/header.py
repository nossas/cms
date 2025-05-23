from cms.api import add_plugin

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from org_nossas.nossas.design.cms_plugins import UICMSPluginBase

from org_nossas.nossas.plugins.models.headermodel import Header, HeaderImage
from org_nossas.nossas.plugins.forms.headerform import HeaderPluginForm, HeaderImagePluginForm


@plugin_pool.register_plugin
class HeaderPlugin(UICMSPluginBase):
    name = "Header"
    module = "NOSSAS"
    model = Header
    form = HeaderPluginForm
    render_template = "nossas/plugins/header.html"
    allow_children = True
    child_classes = [
        "TextPlugin",
    ]
    fieldsets = ((None, {"fields": ["attributes", "background", "graphic_element"]}),)

    def get_form(self, request, obj, change, **kwargs):
        if not change:
            self.form = HeaderPluginForm

        return super().get_form(request, obj, change, **kwargs)

    def create_header_grid(self, obj):
        placeholder = obj.placeholder
        language = obj.language

        # Child plugins

        plugin_type = "TextPlugin"
        child_attrs = {
            "body": """<h1>LOREM IPSUM</h1><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore ut enim ad minim veniam, quis nostrud exercitation.</p>"""
        }
        add_plugin(
            placeholder=placeholder,
            plugin_type=plugin_type,
            language=language,
            target=obj,
            **child_attrs,
        )

    def save_model(self, request, obj, form, change):
        """Change save_model to create plugins by layout"""
        super().save_model(request, obj, form, change)

        if not change:
            self.create_header_grid(obj)


@plugin_pool.register_plugin
class HeaderImagePlugin(UICMSPluginBase):
    name = "Header Imagem + Icone"
    module = "NOSSAS"
    model = HeaderImage
    form = HeaderImagePluginForm
    render_template = "nossas/plugins/header_image.html"
