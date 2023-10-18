from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .forms import PressurePluginForm, PressureAjaxForm
from .models import PressurePluginModel


@plugin_pool.register_plugin
class PressurePlugin(CMSPluginBase):
    name = "Pressão"
    module = "Estrategia"
    render_template = "pressure/pressure_plugin.html"
    model = PressurePluginModel
    form = PressurePluginForm
    cache = False

    def render(self, context, instance, placeholder):
        obj = instance.get_widget()
        request = context["request"]
        initial = (
            {
                "email_subject": obj.settings.get("pressure_subject", ""),
                "email_body": obj.settings.get("pressure_body", ""),
            }
            if obj
            else {}
        )

        form = PressureAjaxForm(initial=initial)

        if instance.reference_id:
            scheme = request.scheme if request.scheme else 'https'
            url = f"{scheme}://{request.get_host()}{request.path}"

            form = PressureAjaxForm(
                initial={
                    "reference_id": instance.reference_id,
                    "referrer_path": url,
                    "whatsapp_text": obj.settings.get("whatsapp_text", url),
                    "twitter_share_text": obj.block.mobilization.twitter_share_text,
                    **initial,
                }
            )

        context.update(
            {
                "form": form,
                "settings": self.get_settings(obj),
                "size": obj.total_actions() if obj else 0,
            }
        )

        return context

    def get_settings(self, obj):
        settings = {
            "title": "Envie um e-mail mandando seu recado",
            "button": "Pressionar",
            "count": "pessoas já pressionaram",
            "main_color": None,
        }

        if obj:
            settings["title"] = (
                obj.settings.get("call_to_action")
                or obj.settings.get("title_text")
                or settings["title"]
            )
            settings["button"] = obj.settings.get("button_text", settings["button"])
            settings["count"] = obj.settings.get("count_text", settings["count"])
            settings["main_color"] = obj.settings.get(
                "main_color", settings["main_color"]
            )

            settings["targets"] = list(
                map(
                    lambda x: dict(
                        name=x.split("<")[0],
                        email=x.split("<")[-1].replace(">", "").replace(";", ""),
                    ),
                    obj.settings.get("targets", []),
                )
            )

        return settings
