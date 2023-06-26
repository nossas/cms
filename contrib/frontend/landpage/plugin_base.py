from cms.plugin_base import CMSPluginBase

from .models import Block
from .forms import LayoutBlockForm
from .layouts import Layout


class BlockPluginBase(CMSPluginBase):
    model = Block
    module = "Landpage"
    render_template = "frontend/landpage/plugins/block.html"
    allow_children = True
    child_classes = [
        "ImagePlugin",
        "TextPlugin",
        "GridPlugin",
        "ButtonPlugin",
        "VideoPlayerPlugin",
        "SnippetPlugin",
    ]
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = [
        (
            None,
            {
                "fields": [
                    ("title", "slug"),
                    ("spacing", "alignment"),
                    ("background_color", "background_image"),
                ]
            },
        ),
        (
            "Opções de exibição",
            {
                "fields": [("hidden", "menu_hidden")],
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

        return super(BlockPluginBase, self).get_form(request, obj, change, **kwargs)

    def get_prepopulated_fields(self, request, obj=None):
        if obj:
            return super(BlockPluginBase, self).get_prepopulated_fields(request, obj)

        return {}

    def get_fieldsets(self, request, obj=None):
        """
        Sobrescreve fieldsets para adicionar atributo layout
        quando estamos criando um Bloco
        """
        fieldsets = super(BlockPluginBase, self).get_fieldsets(request, obj)

        if not obj:
            fieldsets = [
                (
                    None,
                    {"fields": ["layout"]},
                )
            ]

        return fieldsets

    def save_model(self, request, obj, form, change):
        """
        Executa criação de elementos filho ao bloco de acordo
        com o tipo de layout selcionado
        """
        super(BlockPluginBase, self).save_model(request, obj, form, change)

        if not change:
            Layout(obj=obj, layout=form.cleaned_data["layout"]).copy()
