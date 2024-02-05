from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from django.utils.translation import ugettext_lazy as _

from nossas.plugins.models.newslettermodel import NewsletterPluginModel
from nossas.plugins.forms.newsletterform import NewsletterUserForm


@plugin_pool.register_plugin
class NewsletterFormPlugin(CMSPluginBase):
    model = NewsletterPluginModel
    name = _("Formulário de Newsletter")
    render_template = "nossas/plugins/forms/newsletter.html"
    cache = False

    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
            'form': NewsletterUserForm()
        })
        return context