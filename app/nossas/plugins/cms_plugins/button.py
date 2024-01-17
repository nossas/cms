from django.utils.translation import ugettext_lazy as _

from cms.plugin_pool import plugin_pool

from djangocms_frontend.contrib.link.cms_plugins import LinkPlugin

from nossas.plugins.forms.buttonform import LinkButtonForm


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
