from django import forms
from django.db.models import Q

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from contrib.bonde.models import Community

from .models import Navbar, Footer
from .layouts import Layout

from .plugin_base import BlockPluginBase


@plugin_pool.register_plugin
class BlockPlugin(BlockPluginBase):
    name = "Bloco de Conteúdo"


@plugin_pool.register_plugin
class BlockPressurePlugin(BlockPluginBase):
    name = "Bloco de Pressão"
    fields = []

    def get_form(self, request, obj, change, **kwargs):
        """
        Sobrescreve formulário para adicionar Pressão como layout padrão
        """
        form = super(BlockPressurePlugin, self).get_form(request, obj, change, **kwargs)

        if not change:
            form.base_fields["layout"].initial = "pressure"
            form.base_fields["layout"].widget = forms.HiddenInput()

        return form


@plugin_pool.register_plugin
class NavbarPlugin(CMSPluginBase):
    name = "Navbar"
    module = "Frontend"
    model = Navbar
    render_template = "frontend/landpage/plugins/navbar.html"
    allow_children = False

    def render(self, context, instance, placeholder):
        context = super(NavbarPlugin, self).render(context, instance, placeholder)

        current_page = context["request"].current_page

        placeholder = current_page.get_placeholders().get(slot="content")

        if placeholder:
            plugins = (
                placeholder.get_child_plugins()
                .filter(Q(plugin_type="BlockPlugin") | Q(plugin_type="BlockPressurePlugin"))
                .order_by("position")
            )

            context["children"] = list(
                filter(
                    lambda x: not x.menu_hidden and not x.hidden,
                    map(lambda x: x.get_bound_plugin(), plugins),
                )
            )
        else:
            context["children"] = list()

        return context


@plugin_pool.register_plugin
class FooterPlugin(CMSPluginBase):
    name = "Footer"
    module = "Frontend"
    model = Footer
    render_template = "frontend/landpage/plugins/footer.html"
    allow_children = False

    def render(self, context, instance, placeholder):
        context = super(FooterPlugin, self).render(context, instance, placeholder)
        request = context["request"]

        community = Community.objects.on_site(request).first()
        context.update({"community": community})

    
   

        return context
