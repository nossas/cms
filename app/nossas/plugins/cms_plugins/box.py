from cms.api import add_plugin

# from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from djangocms_text_ckeditor.utils import plugin_to_tag

from nossas.design.cms_plugins import UICMSPluginBase
from nossas.plugins.models.boxmodel import Box
from nossas.plugins.forms.boxform import BoxPluginForm, LayoutBoxPluginForm


@plugin_pool.register_plugin
class BoxPlugin(UICMSPluginBase):
    name = "Box"
    module = "NOSSAS"
    model = Box
    form = BoxPluginForm
    render_template = "nossas/plugins/box.html"
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

    def get_form(self, request, obj, change, **kwargs):
        if not change:
            self.form = LayoutBoxPluginForm

        return super().get_form(request, obj, change, **kwargs)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            self.fieldsets = (
                (None, {"fields": ["attributes", "layout"]}),
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

    def create_header_box(self, obj):
        placeholder = obj.placeholder
        language = obj.language

        # Child plugins

        # Add Image inside Box
        plugin_type = "PicturePlugin"
        child_attrs = {
            # Define fake image
            "external_picture": "http://via.placeholder.com/640x360",
            "template": "background",
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

    def create_cta_box(self, obj):
        placeholder = obj.placeholder
        language = obj.language

        # Configure attributes default
        obj.attributes.update(
            {
                "padding": [
                    {"side": "y", "spacing": "3"},
                    {"side": "x", "spacing": "5"},
                ]
            }
        )
        obj.save()

        # Child plugins

        # Text Plugin
        plugin_type = "TextPlugin"
        child_attrs = {
            "body": """<h1 style="text-align: center;">Lorem ipsum</h1><p style="text-align: center;">Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur.</p>"""
        }
        text = add_plugin(
            placeholder=placeholder,
            plugin_type=plugin_type,
            language=language,
            target=obj,
            **child_attrs,
        )

        # Adiciona link dentro do editor de texto
        plugin_type = "MyLinkPlugin"
        child_attrs = {"config": {"link_type": "btn", "external_link": "https://nossas.org", "name": "Call to action"}}
        text_child_1 = add_plugin(
            placeholder=placeholder,
            plugin_type=plugin_type,
            language=language,
            target=text,
            **child_attrs,
        )

        text.body = f'{text.body}<p style="text-align: center;">{plugin_to_tag(text_child_1)}</p>'
        text.save()
        

    def save_model(self, request, obj, form, change):
        """Change save_model to create plugins by layout"""
        super().save_model(request, obj, form, change)

        if not change and form.cleaned_data["layout"]:
            layout = form.cleaned_data["layout"]
            getattr(self, f"create_{layout}_box")(obj)
