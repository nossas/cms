from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import Navbar, Menu, MenuExtraLink
from .forms import MenuExtraLinkForm


@plugin_pool.register_plugin
class NavbarPlugin(CMSPluginBase):
    name = _("Navbar")
    model = Navbar
    render_template = "ds/plugins/navbar.html"
    allow_children = True

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        css_styles = []
        css_classes = ['navbar', 'navbar-expand-lg']

        if instance.placement:
            css_classes.append(f"{instance.placement}")

        if instance.alignment:
            css_styles.append(f"justify-content:{instance.alignment}")

        context["css_styles"] = ";".join(css_styles)
        context["css_classes"] = " ".join(css_classes)
        return context


@plugin_pool.register_plugin
class FooterPlugin(CMSPluginBase):
    name = _("Rodapé")
    # model = Navbar
    render_template = "ds/plugins/footer.html"
    allow_children = True


class LinkInlineAdmin(admin.StackedInline):
    model = MenuExtraLink
    form = MenuExtraLinkForm


@plugin_pool.register_plugin
class MenuPlugin(CMSPluginBase):
    name = _("Menu")
    model = Menu
    render_template = "ds/plugins/menu.html"
    inlines = (LinkInlineAdmin,)

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        css_styles = []

        if instance.color:
            h = instance.color.lstrip("#")
            rgba = "rgba(" + ",".join(tuple(str(int(h[i:i+2], 16)) for i in (0, 2, 4)))

            css_styles.append(f"--bs-nav-link-color:{rgba},1)")
            css_styles.append(f"--bs-nav-link-hover-color:{rgba},.75)")
            if instance.active_styled:
                css_styles.append(f"--bs-navbar-active-color:{rgba},1)")
            else:
                css_styles.append(f"--bs-navbar-active-color:{rgba},.75)")
        
        context["css_styles"] = ";".join(css_styles)
        context["extra_links"] = MenuExtraLink.objects.filter(menu_plugin=instance)
        
        return context
