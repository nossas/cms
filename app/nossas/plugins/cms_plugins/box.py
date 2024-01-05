from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from nossas.design.cms_plugins import (
    UIPaddingMixin,
    UIBackgroundMixin,
    UIBorderMixin,
    CMSUIPlugin,
)
from nossas.plugins.models.boxmodel import Box
from nossas.plugins.forms.boxform import BoxPluginForm, LayoutBoxPluginForm


@plugin_pool.register_plugin
class BoxPlugin(UIBorderMixin, UIPaddingMixin, UIBackgroundMixin, CMSUIPlugin):
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

    def save_model(self, request, obj, form, change):
        """Change save_model to create plugins by layout"""
        super().save_model(request, obj, form, change)

        if not change and form.cleaned_data["layout"]:
            # create plugin by layout
            from cms.api import add_plugin

            if form.cleaned_data["layout"] == "header":
                placeholder = obj.placeholder
                language = obj.language

                # Child plugins

                # Add Image inside Box
                plugin_type = "ImagePlugin"
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
                    **child_attrs
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
                    **child_attrs
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
                    **child_attrs
                )
