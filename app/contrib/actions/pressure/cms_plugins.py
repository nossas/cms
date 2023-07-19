from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .forms import PressurePluginForm, PressureAjaxForm
from .models import PressurePluginModel


@plugin_pool.register_plugin
class PressurePlugin(CMSPluginBase):
    name = "Pressão"
    module = "Estrategia"
    # render_template = "pressure/pressure_plugin.html"
    # render_template = "pressure/tweet_button.html"
    render_template = "pressure/instagram_inc.html"
    model = PressurePluginModel
    form = PressurePluginForm

    def render(self, context, instance, placeholder):
        obj = instance.get_widget()
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
            form = PressureAjaxForm(
                initial={"reference_id": instance.reference_id, **initial}
            )

        context.update(
            {
                "form": form,
                "settings": self.get_settings(obj),
                "size": obj.total_actions() if obj else 0,
                "tweet": {
                    "message": self.encode_tweet("IMPORTANTE: @nossas_ queremos #tarifazero já https://nossas.org"),
                }
            }
        )

        return context

    def encode_tweet(self, msg):
        """Fix caracteres not permitted in urlparams"""
        return msg.replace("#", "%23")

    def get_settings(self, obj):
        settings = {
            "title": "Envie um e-mail mandando seu recado",
            "button": "Pressionar",
            "count": "pessoas já pressionaram",
        }

        if obj:
            settings["title"] = obj.settings.get("title_text", settings["title"])
            settings["button"] = obj.settings.get("button_text", settings["button"])
            settings["count"] = obj.settings.get("count_text", settings["count"])

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
