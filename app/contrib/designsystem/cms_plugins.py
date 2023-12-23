from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from djangocms_frontend.contrib.accordion.cms_plugins import (
    AccordionPlugin,
    AccordionItemPlugin,
)

from .forms import DSForm


class DSCardPlugin(CMSPluginBase):
    render_template = "ds/plugins/card.html"


plugin_pool.register_plugin(DSCardPlugin)


class DSHeadingPlugin(CMSPluginBase):
    render_template = "ds/plugins/heading.html"


plugin_pool.register_plugin(DSHeadingPlugin)


class DSBreaklinePlugin(CMSPluginBase):
    render_template = "ds/plugins/breakline.html"


plugin_pool.register_plugin(DSBreaklinePlugin)


class DSAccordionPlugin(AccordionPlugin):
    name = "DSAccordionPlugin"
    render_template = "ds/plugins/accordion.html"
    child_classes = [
        "DSAccordionItemPlugin",
    ]


plugin_pool.register_plugin(DSAccordionPlugin)


class DSAccordionItemPlugin(AccordionItemPlugin):
    name = "DSAccordionItemPlugin"
    render_template = "ds/plugins/accordion_item.html"
    parent_classes = [
        "DSAccordionPlugin",
    ]


plugin_pool.register_plugin(DSAccordionItemPlugin)


class DSModalPlugin(CMSPluginBase):
    render_template = "ds/plugins/modal.html"


plugin_pool.register_plugin(DSModalPlugin)


class DSFormPlugin(CMSPluginBase):
    render_template = "ds/plugins/form.html"

    def render(self, context, instance, placeholder):
        context = super(DSFormPlugin, self).render(context, instance, placeholder)
        context["form"] = DSForm()

        return context


plugin_pool.register_plugin(DSFormPlugin)
