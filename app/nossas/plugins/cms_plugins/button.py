from django.utils.translation import ugettext_lazy as _

from cms.plugin_pool import plugin_pool

from djangocms_frontend.contrib.link.cms_plugins import LinkPlugin

from nossas.plugins.forms.buttonform import LinkButtonForm


@plugin_pool.register_plugin
class LinkButtonPlugin(LinkPlugin):
    name = _("Link / Botão")
    module = "NOSSAS"
    form = LinkButtonForm
