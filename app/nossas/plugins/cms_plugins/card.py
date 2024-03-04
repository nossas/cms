from cms.api import add_plugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from nossas.design.cms_plugins import UICMSPluginBase

from ..models.cardmodel import Card
from ..forms.cardform import CreateCardPluginForm, CardPluginForm


@plugin_pool.register_plugin
class CardPlugin(UICMSPluginBase):
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
            return CardPluginForm

    def get_fieldsets(self, request, obj=None):
        if obj:
            return (
                (None, {
                    "fields": ["image", "tag"],
                }),
                ("Link", {
                    "fields": ["internal_link", "external_link", "target"],
                    "classes": ["collapse"]
                })
            )

        return (
            (None, {
                "fields": ["image", "tag", "title", "description"],
            }),
            ("Link", {
                "fields": ["internal_link", "external_link", "target"],
                "classes": ["collapse"]
            })
        )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change:
            placeholder = obj.placeholder
            language = obj.language

            # Child plugins

            title = form.cleaned_data.get("title", "TÍTULO EM ATÉ 2 LINHAS")
            description = form.cleaned_data.get("description")

            # Text Plugin
            plugin_type = "TextPlugin"
            if description:
                child_attrs = {"body": f"""<h2>{title}</h2><p>{description}</p>"""}
            else:
                child_attrs = {"body": f"""<h2>{title}</h2>"""}

            add_plugin(
                placeholder=placeholder,
                plugin_type=plugin_type,
                language=language,
                target=obj,
                **child_attrs,
            )

    def render(self, context, instance, placeholder):
        context['link'] = instance.get_link()
        return super().render(context, instance, placeholder)