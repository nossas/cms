from django.utils.translation import gettext_lazy as _

from cms.cms_plugins import CMSPluginBase, plugin_pool

from .forms import PublicationListForm
from .models import Publication, PublicationList


@plugin_pool.register_plugin
class PublicationListPlugin(CMSPluginBase):
    name = _("Listagem de Publicações")
    module = "NOSSAS"
    model = PublicationList
    form = PublicationListForm
    render_template = "nossas/publications/publication_list_plugin.html"

    # def get_form(self, request, obj=None, change=False, **kwargs):
    #     form = super().get_form(request, obj, change, **kwargs)
        
    #     import ipdb;ipdb.set_trace()
    #     if not change and request.current_page.application_namespace:
    #         form.fields["category"].initial = request.current_page

    #     return form


    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        qs = Publication.on_site.all()

        if instance.category:
            qs = qs.filter(parent=instance.category)

        context["publication_list"] = qs
        
        return context