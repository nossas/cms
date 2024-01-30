from cms.api import add_plugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from ..models.cardmodel import Card
from ..forms.cardform import CreateCardPluginForm


@plugin_pool.register_plugin
class CardPlugin(CMSPluginBase):
    name = "Card"
    module = "NOSSAS"
    model = Card
    allow_children = True
    child_classes = ["TextPlugin"]
    render_template = "nossas/plugins/card.html"

    def get_form(self, request, obj=None, change=False, **kwargs):
        if not change:
            return CreateCardPluginForm
        else:
            return super().get_form(request, obj, change, **kwargs)

    def get_fields(self, request, obj=None):
        if obj:
            return ["image", "tag"]
        return super().get_fields(request, obj)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change:
            placeholder = obj.placeholder
            language = obj.language

            # Child plugins

            title = form.cleaned_data.get("title", "TÍTULO EM ATÉ 2 LINHAS")
            description = form.cleaned_data.get(
                "description",
                "Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur.",
            )

            # Text Plugin
            plugin_type = "TextPlugin"
            child_attrs = {"body": f"""<h2>{title}</h2><p>{description}</p>"""}
            add_plugin(
                placeholder=placeholder,
                plugin_type=plugin_type,
                language=language,
                target=obj,
                **child_attrs,
            )
