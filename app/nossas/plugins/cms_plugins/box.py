from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from nossas.design.cms_plugins import (
    UIPaddingMixin,
    UIBackgroundMixin,
    UIBorderMixin,
    CMSUIPlugin,
)
from nossas.plugins.models.boxmodel import Box
from nossas.plugins.forms.boxform import BoxPluginForm


@plugin_pool.register_plugin
class BoxPlugin(UIPaddingMixin, UIBackgroundMixin, UIBorderMixin, CMSUIPlugin):
    name = "Box"
    module = "NOSSAS"
    model = Box
    form = BoxPluginForm
    render_template = "nossas/plugins/box.html"
    allow_children = True