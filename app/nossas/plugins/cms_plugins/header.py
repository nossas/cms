from cms.api import add_plugin

from cms.plugin_pool import plugin_pool

from nossas.design.cms_plugins import UICMSPluginBase

from nossas.plugins.models.headermodel import Header
from nossas.plugins.forms.headerform import HeaderPluginForm

@plugin_pool.register_plugin
class HeaderPlugin(UICMSPluginBase):
    name = "Header"
    module = "NOSSAS"
    model = Header
    form = HeaderPluginForm
    render_template = "nossas/plugins/header.html"
    allow_children = True
    fieldsets = (
        ("Atributos", {"fields": ["attributes"]}),
        ("Fundo", {"fields": ["background"]})
    )

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        picture_urls = []

        for child_plugin in instance.child_plugin_instances:
            if child_plugin.plugin_type == 'PicturePlugin':
                picture_url = child_plugin.external_picture or (child_plugin.picture.url if child_plugin.picture else None)
                if picture_url:
                    picture_urls.append(picture_url)

        context['picture_urls'] = picture_urls

        return context

    def get_form(self, request, obj, change, **kwargs):
        if not change:
            self.form = HeaderPluginForm

        return super().get_form(request, obj, change, **kwargs)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            self.fieldsets = (
                (None, {"fields": ["attributes"]}),
                ("Fundo", {"fields": ["background"]}),
            )

        return super().get_fieldsets(request, obj)

    def create_header_grid(self, obj):
        placeholder = obj.placeholder
        language = obj.language

        # Child plugins

        # Add Image inside Box
        plugin_type = "PicturePlugin"
        child_attrs = {
            # Define fake image
            "external_picture": "http://via.placeholder.com/640x360",
            "height": 360,
        }
        add_plugin(
            placeholder=placeholder,
            plugin_type=plugin_type,
            language=language,
            target=obj,
            **child_attrs,
        )

        # Add Box inside Box
        plugin_type = "BoxPlugin"
        child_attrs = {
            "attributes": {
                "padding": [
                    {"side": "t", "spacing": "3"},
                    {"side": "b", "spacing": "4"},
                    {"side": "x", "spacing": "5"},
                ]
            }
        }
        obj = add_plugin(
            placeholder=placeholder,
            plugin_type=plugin_type,
            language=language,
            target=obj,
            **child_attrs,
        )

        # Add Text inside new Box
        plugin_type = "TextPlugin"
        child_attrs = {
            "body": """<h1>Lorem ipsum</h1><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore ut enim ad minim veniam, quis nostrud exercitation.</p>"""
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
