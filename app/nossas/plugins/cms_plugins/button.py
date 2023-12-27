from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from nossas.design.cms_plugins import UIPaddingMixin, UIBackgroundMixin, CMSUIPlugin
from nossas.plugins.models.buttonmodel import Button
from nossas.plugins.forms.buttonform import ButtonPluginForm


@plugin_pool.register_plugin
class DSButtonPlugin(UIPaddingMixin, UIBackgroundMixin, CMSUIPlugin):
    name = "Botão"
    module = "NOSSAS"
    model = Button
    form = ButtonPluginForm
    render_template = "nossas/plugins/button.html"
    allow_children = True
    text_enabled = True