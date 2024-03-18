from cms.api import add_plugin

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from nossas.plugins.models.accordionmodel import AccordionItem


@plugin_pool.register_plugin
class AccordionPlugin(CMSPluginBase):
    name = "Acordeão"
    module = "NOSSAS"
    render_template = "nossas/plugins/accordion.html"
    allow_children = True
    child_classes = ["AccordionItemPlugin"]

    def add_default_item(self, obj):
        placeholder = obj.placeholder
        language = obj.language

        plugin_type = "AccordionItemPlugin"
        child_attrs = {
            "title": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor qui adipisci velit, sed qut enim ad minima?"
        }
        target = add_plugin(
            placeholder=placeholder,
            plugin_type=plugin_type,
            language=language,
            target=obj,
            **child_attrs,
        )

        plugin_type = "TextPlugin"
        child_attrs = {
            "body": """<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore ut enim ad minim veniam, quis nostrud exercitation.</p>"""
        }
        add_plugin(
            placeholder=placeholder,
            plugin_type=plugin_type,
            language=language,
            target=target,
            **child_attrs,
        )

    def save_model(self, request, obj, form, change):
        """Change save_model to create plugins by layout"""
        super().save_model(request, obj, form, change)

        if not change:
            self.add_default_item(obj)


@plugin_pool.register_plugin
class AccordionItemPlugin(CMSPluginBase):
    name = "Acordeão Item"
    module = "NOSSAS"
    model = AccordionItem
    render_template = "nossas/plugins/accordion_item.html"
    allow_children = True
    parent_classes = ["AccordionPlugin"]

    def add_default_text(self, obj):
        placeholder = obj.placeholder
        language = obj.language

        plugin_type = "TextPlugin"
        child_attrs = {
            "body": """<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore ut enim ad minim veniam, quis nostrud exercitation.</p>"""
        }
        obj = add_plugin(
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
            self.add_default_text(obj)
