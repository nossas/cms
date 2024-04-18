from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import Accordion, AccordionItem


@plugin_pool.register_plugin
class AccordionPlugin(CMSPluginBase):
    name = "Acordeão"
    model = Accordion
    render_template = "accordion/plugins/accordion.html"
    allow_children = True
    child_classes = ["AccordionItemPlugin"]


@plugin_pool.register_plugin
class AccordionItemPlugin(CMSPluginBase):
    name = "Acordeão Item"
    model = AccordionItem
    render_template = "accordion/plugins/accordion_item.html"
    allow_children = True
    require_parent = True
    parent_classes = ["AccordionPlugin"]