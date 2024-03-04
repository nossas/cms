from cms.api import add_plugin

# from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from djangocms_text_ckeditor.utils import plugin_to_tag

from nossas.design.cms_plugins import UICMSPluginBase
from nossas.plugins.models.boxmodel import Box
from nossas.plugins.forms.boxform import BoxPluginForm, LayoutBoxPluginForm


@plugin_pool.register_plugin
class BoxPlugin(UICMSPluginBase):
    name = "Box CTA"
    module = "NOSSAS"
    model = Box
    form = BoxPluginForm
    render_template = "nossas/plugins/box.html"
    allow_children = True
    child_classes = ["TextPlugin", "SocialSharePlugin", "LinkButtonPlugin"]
    fieldsets = (
        (None, {"fields": ["attributes"]}),
        ("Cores", {"fields": ["background", "color"]}),
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
            )

        return super().get_fieldsets(request, obj)


    def create_cta_box(self, obj):
        placeholder = obj.placeholder
        language = obj.language

        # Child plugins

        # Text Plugin
        plugin_type = "TextPlugin"
        child_attrs = {
            "body": """<h2 style="text-align: center;">LOREM IPSUM</h2><p style="text-align: center;">Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur.</p>"""
        }
        add_plugin(
            placeholder=placeholder,
            plugin_type=plugin_type,
            language=language,
            target=obj,
            **child_attrs,
        )

        # Adiciona link dentro do editor de texto
        plugin_type = "LinkButtonPlugin"
        child_attrs = {
            "config": {
                "link_outline": False,
                "link_context": obj.attributes.get("color").replace("bg-", ""),
                "link_type": "btn",
                "external_link": "https://nossas.org",
                "name": "Call to action",
                "attributes": {
                    "class": obj.attributes.get("background").replace("bg-", "text-")
                },
            }
        }
        add_plugin(
            placeholder=placeholder,
            plugin_type=plugin_type,
            language=language,
            target=obj,
            **child_attrs,
        )

    def create_share_box(self, obj):
        placeholder = obj.placeholder
        language = obj.language

        # Child plugins

        # Text Plugin
        plugin_type = "TextPlugin"
        child_attrs = {
            "body": """<h2 style="text-align: center;">LOREM IPSUM</h2><p style="text-align: center;">Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur.</p>"""
        }
        add_plugin(
            placeholder=placeholder,
            plugin_type=plugin_type,
            language=language,
            target=obj,
            **child_attrs,
        )

        # SocialShare Plugin
        plugin_type = "SocialSharePlugin"
        child_attrs = {
            "selected_social_media": "facebook,linkedin,twitter,whatsapp"
        }
        add_plugin(
            placeholder=placeholder,
            plugin_type=plugin_type,
            language=language,
            target=obj,
            **child_attrs,
        )

        # Adiciona link dentro do editor de texto
        plugin_type = "LinkButtonPlugin"
        child_attrs = {
            "config": {
                "link_outline": False,
                "link_context": obj.attributes.get("color").replace("bg-", ""),
                "link_type": "btn",
                "external_link": "https://nossas.org",
                "name": "Call to action",
                "attributes": {
                    "class": obj.attributes.get("background").replace("bg-", "text-")
                },
            }
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

        if not change and form.cleaned_data["layout"]:
            layout = form.cleaned_data["layout"]
            getattr(self, f"create_{layout}_box")(obj)
