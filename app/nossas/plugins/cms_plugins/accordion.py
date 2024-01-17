from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from nossas.plugins.models.accordionmodel import Accordion


@plugin_pool.register_plugin
class AccordionPlugin(CMSPluginBase):
    name = "Accordion"
    module = "NOSSAS"
    model = Accordion
    render_template = "nossas/plugins/accordion.html"
    allow_children = True
