from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from nossas.design.cms_plugins import UIBackgroundMixin, CMSUIPlugin
from nossas.plugins.models.navbarmodel import Navbar
from nossas.plugins.forms.navbarform import NavbarPluginForm


@plugin_pool.register_plugin
class NossasNavbarPlugin(UIBackgroundMixin, CMSUIPlugin):
    name = "Navbar"
    module = "NOSSAS"
    model = Navbar
    form = NavbarPluginForm
    render_template = "nossas/plugins/navbar.html"
