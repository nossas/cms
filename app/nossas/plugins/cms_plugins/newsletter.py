from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from django.utils.translation import ugettext_lazy as _

from contrib.bonde.api import create_form_entry
from nossas.plugins.models.newslettermodel import NewsletterPluginModel
from nossas.plugins.forms.newsletterform import NewsletterSignUpForm, NewsletterPluginForm


@plugin_pool.register_plugin
class NewsletterFormPlugin(CMSPluginBase):
    model = NewsletterPluginModel
    form = NewsletterPluginForm
    name = _("Formulário de Newsletter")
    render_template = "nossas/plugins/forms/newsletter.html"
    cache = False

    def render(self, context, instance, placeholder):
        request = context.get("request")
        if request.method == "POST":
            form = NewsletterSignUpForm(request.POST)
            if form.is_valid():
                try:
                    create_form_entry(settings = instance.config, **form.cleaned_data)
                    context.update({
                        "template": "nossas/plugins/forms/newsletter_success.html",
                        "name": form.cleaned_data["name"],
                        "email": form.cleaned_data["email"]
                    })
                except Exception as err:
                    context.update({
                        "template": "nossas/plugins/forms/newsletter_error.html",
                        "form": form,
                        "error_message": err
                    })
        else:
            form = NewsletterSignUpForm()
        
        context.update({"form": form})
        return super().render(context, instance, placeholder)
