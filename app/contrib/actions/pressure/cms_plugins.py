from typing import Any
from django.contrib import admin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

# from .forms.base import PressureAdminForm, PressureAdminChangeForm
from .forms.plugins_form import PressurePluginAddForm, PressureAjaxForm
from .models.plugins import PressurePluginModel
from .models.base import EmailPressure, PhonePressure, TwitterPressure

# from .admin import EmailPressureInline, PhonePressureInline, TwitterPressureInline


class EmailPressureInline(admin.StackedInline):
    model = EmailPressure
    extra = 1
    max_num = 1
    template = "pressure/admin/pressure_inline_formset.html"


class PhonePressureInline(admin.StackedInline):
    model = PhonePressure
    extra = 1
    max_num = 1
    template = "pressure/admin/pressure_inline_formset.html"


class TwitterPressureInline(admin.StackedInline):
    model = TwitterPressure
    extra = 1
    max_num = 1
    template = "pressure/admin/pressure_inline_formset.html"


@plugin_pool.register_plugin
class PressurePlugin(CMSPluginBase):
    name = "Pressão"
    module = "Estrategia"
    render_template = "pressure/pressure_plugin.html"
    # change_form_template = "admin2/pressure_plugin/change_form.html"
    # render_template = "pressure/tweet_button.html"
    # render_template = "pressure/instagram_inc.html"
    model = PressurePluginModel
    # related_action_model = Pressure
    form = PressurePluginAddForm
    # change_form_template = "pressure/admin/pressure_change_form.html"
    # inlines = (EmailPressureInline, PhonePressureInline, TwitterPressureInline)

    class Media:
        js = ["pressure/js/tabs.js"]

    def render(self, context, instance, placeholder):
        # obj = instance.get_widget()
        # total_actions = obj.total_actions() if obj else 0
        # settings = self.get_settings(obj)
        obj = None
        total_actions = 0
        settings = {
            "pressure_subject": "Valor padrão alterar",
            "pressure_body": "Valor padrão alterar"
        }

        initial = (
            {
                "email_subject": settings.get("pressure_subject", ""),
                "email_body": settings.get("pressure_body", ""),
                "total_actions": f"{total_actions} {settings.get('count')}",
            }
        )

        form = PressureAjaxForm(initial=initial)

        if instance.action_id:
            form = PressureAjaxForm(
                initial={"action_id": instance.action_id, **initial}
            )

        context.update(
            {
                "form": form,
                "settings": settings,
                "size": total_actions,
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
