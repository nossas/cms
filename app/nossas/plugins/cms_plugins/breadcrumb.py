from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from nossas.design.cms_plugins import UICMSPluginBase

from ..forms.breadcrumbform import BreadcrumbPluginForm
from ..models.breadcrumbmodel import Breadcrumb


@plugin_pool.register_plugin
class BreadcrumbPlugin(UICMSPluginBase):
    name = "Breadcrumb"
    module = "NOSSAS"
    model = Breadcrumb
    form = BreadcrumbPluginForm
    render_template = "nossas/plugins/breadcrumb.html"
