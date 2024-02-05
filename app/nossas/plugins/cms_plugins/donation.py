from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from django.utils.translation import ugettext_lazy as _

from nossas.plugins.models.donationmodel import DonationPluginModel
from nossas.plugins.forms.donationform import DonationUserForm


@plugin_pool.register_plugin
class DonationFormPlugin(CMSPluginBase):
    model = DonationPluginModel
    name = _("Formulário de Doação")
    render_template = "nossas/plugins/forms/donation.html"
    cache = False

    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
            'form': DonationUserForm()
        })
        return context
