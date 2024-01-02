from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool


@plugin_pool.register_plugin
class BreadcrumbPlugin(CMSPluginBase):
    name = "Breadcrumb"
    module = "NOSSAS"
    render_template = "nossas/plugins/breadcrumb.html"