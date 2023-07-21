from typing import Any
from django.contrib import admin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.http.request import HttpRequest
from django.http.response import HttpResponse

# from .forms.base import PressureAdminForm, PressureAdminChangeForm
from .forms.plugins import PressurePluginAddForm, PressureAjaxForm
from .models.plugins import PressurePluginModel
from .models.base import Pressure, EmailPressure, PhonePressure, TwitterPressure
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
    render_template = "pressure/pressure_plugin_2.html"
    # render_template = "pressure/tweet_button.html"
    # render_template = "pressure/instagram_inc.html"
    model = PressurePluginModel
    # related_action_model = Pressure
    form = PressurePluginAddForm
    # change_form_template = "pressure/admin/pressure_change_form.html"
    # inlines = (EmailPressureInline, PhonePressureInline, TwitterPressureInline)

    class Media:
        js = ["pressure/js/tabs.js"]

    # def get_inline_instances(self, request, obj=None):
    #     inline_instances = []
    #     for inline_class in self.get_inlines(request, obj):
    #         inline = inline_class(self.related_action_model, self.admin_site)
    #         if request:
    #             if not (inline.has_view_or_change_permission(request, obj) or
    #                     inline.has_add_permission(request, obj) or
    #                     inline.has_delete_permission(request, obj)):
    #                 continue
    #             if not inline.has_add_permission(request, obj):
    #                 inline.max_num = 0
    #         inline_instances.append(inline)

    #     return inline_instances

    # def get_form(self, request, obj, change=False, **kwargs: Any) -> Any:
    #     if change:
    #         self.form = PressureAdminChangeForm
    #     return super().get_form(request, obj, change, **kwargs)
    

    # def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
    #     if change:
    #         obj.campaign = obj.campaign.id
    #     return super().save_model(request, obj, form, change)

    # def render(self, context, instance, placeholder):
    #     obj = instance.get_widget()
    #     initial = (
    #         {
    #             "email_subject": obj.settings.get("pressure_subject", ""),
    #             "email_body": obj.settings.get("pressure_body", ""),
    #         }
    #         if obj
    #         else {}
    #     )

    #     form = PressureAjaxForm(initial=initial)

    #     if instance.reference_id:
    #         form = PressureAjaxForm(
    #             initial={"reference_id": instance.reference_id, **initial}
    #         )

    #     context.update(
    #         {
    #             "form": form,
    #             "settings": self.get_settings(obj),
    #             "size": obj.total_actions() if obj else 0,
    #             "tweet": {
    #                 "message": self.encode_tweet("IMPORTANTE: @nossas_ queremos #tarifazero já https://nossas.org"),
    #             }
    #         }
    #     )

    #     return context

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
