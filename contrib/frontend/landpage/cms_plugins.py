# BlockPlugin
# utils (layout)

# Navbar
# Footer
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from contrib.bonde.models import Community

from .models import Block, Navbar, Footer
from .forms import LayoutBlockForm
from .layouts import Layout


@plugin_pool.register_plugin
class BlockPlugin(CMSPluginBase):
    model = Block
    name = "Bloco"
    module = "Frontend"
    render_template = "frontend/landpage/plugins/block.html"
    allow_children = True
    child_classes = ["PicturePlugin", "TextPlugin", "GridPlugin", "ButtonPlugin"]
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = [
        (
            None,
            {"fields": [("title", "slug"), ("spacing", "alignment")]},
        ),
        ("Background", {"fields": [("background_color", "background_image")]}),
        (
            "Opções avançadas",
            {
                "classes": ["collapse"],
                "fields": ["menu_title", "menu_hidden", "hidden"],
            },
        ),
    ]

    def get_form(self, request, obj, change, **kwargs):
        """
        Sobrescreve formulário para adicionar atributo layout
        quando estamos criando um Bloco
        """
        if not change:
            self.form = LayoutBlockForm

        return super(BlockPlugin, self).get_form(request, obj, change, **kwargs)

    def get_fieldsets(self, request, obj=None):
        """
        Sobrescreve fieldsets para adicionar atributo layout
        quando estamos criando um Bloco
        """
        fieldsets = super(BlockPlugin, self).get_fieldsets(request, obj)

        if not obj:
            fieldsets[0] = (
                None,
                {"fields": [("title", "slug"), ("spacing", "layout")]},
            )
        else:
            fieldsets[0] = (
                None,
                {"fields": [("title", "slug"), ("spacing", "alignment")]},
            )

        return fieldsets

    def save_model(self, request, obj, form, change):
        """
        Executa criação de elementos filho ao bloco de acordo
        com o tipo de layout selcionado
        """
        super(BlockPlugin, self).save_model(request, obj, form, change)

        if not change:
            Layout(obj=obj, layout=form.cleaned_data["layout"]).copy()


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
                .filter(plugin_type="BlockPlugin")
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
        request = context['request']

        community = Community.objects.on_site(request).first()
        context.update({"community": community})

        return context

