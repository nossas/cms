from django.utils.translation import gettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import Navbar


@plugin_pool.register_plugin
class NavbarPlugin(CMSPluginBase):
    name = _("Navbar")
    model = Navbar
    render_template = "ds/plugins/navbar.html"


@plugin_pool.register_plugin
class FooterPlugin(CMSPluginBase):
    name = _("Footer")
    # model = Navbar
    render_template = "ds/plugins/footer.html"
    allow_children = True