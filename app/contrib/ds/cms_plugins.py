from django.utils.translation import gettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import Navbar


@plugin_pool.register_plugin
class NavbarPlugin(CMSPluginBase):
    name = _("Navbar")
    model = Navbar
    render_template = "ds/plugins/navbar.html"
    allow_children = True

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        css_styles = []

        if instance.alignment:
            css_styles.append(f"justify-content:{instance.alignment}")

        context["css_styles"] = ";".join(css_styles)
        return context


@plugin_pool.register_plugin
class FooterPlugin(CMSPluginBase):
    name = _("Rodapé")
    # model = Navbar
    render_template = "ds/plugins/footer.html"
    allow_children = True
