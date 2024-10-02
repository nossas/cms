from cms.plugin_pool import plugin_pool

from org_nossas.nossas.design.cms_plugins import UICMSPluginBase
from org_nossas.nossas.plugins.models.headlinemodel import Headline
from org_nossas.nossas.plugins.forms.headlineform import HeadlineForm


@plugin_pool.register_plugin
class HeadlinePlugin(UICMSPluginBase):
    name = "Headline"
    module = "NOSSAS"
    model = Headline
    form = HeadlineForm
    allow_children = True
    child_classes = ["TextPlugin"]
    render_template = "nossas/plugins/headline.html"
