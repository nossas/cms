from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from djangocms_frontend.contrib.link.cms_plugins import LinkPlugin

from nossas.plugins.forms.buttonform import LinkButtonForm

# from nossas.design.cms_plugins import UIPaddingMixin, UIBackgroundMixin, CMSUIPlugin
# from nossas.plugins.models.buttonmodel import Button
# from nossas.plugins.forms.buttonform import ButtonPluginForm


@plugin_pool.register_plugin
class LinkButtonPlugin(LinkPlugin):
    name = _("Link / Botão")
    module = "NOSSAS"
    form = LinkButtonForm
    # change_form_template = 'nossas/admin/link.html'
#     model = Button
#     form = ButtonPluginForm
#     render_template = "nossas/plugins/button.html"
#     allow_children = True
#     text_enabled = True
