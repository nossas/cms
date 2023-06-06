from django.contrib import admin
from django.db.models import Q

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from contrib.bonde.models import Widget

from .models import Pressure, TargetGroup
from .forms import PressureForm, PressureSettingsForm


class TargetGroupInline(admin.StackedInline):
    model = TargetGroup


@plugin_pool.register_plugin
class PressurePlugin(CMSPluginBase):
    name = "Pressão"
    render_template = "campaign/plugins/pressure.html"
    change_form_template = "campaign/admin/change_form.html"
    model = Pressure
    form = PressureSettingsForm
    inlines = [TargetGroupInline, ]
    fieldsets = [
        ("Alvos", {"fields": ["is_group"], "classes": ["tab-active"]}),
        ("Email", {"fields": ["disable_editing"]}),
        (
            "Envio",
            {
                "fields": ["submissions_limit", "submissions_interval"],
            },
        ),
        (
            "Agradecimento",
            {
                "fields": [
                    "email_subject",
                    "sender_name",
                    "sender_email",
                    "email_body",
                ],
            },
        ),
        ("Pós-ação", {"fields": ["sharing", "whatsapp_text"]}),
    ]

    # def get_form(self, request, obj=None, change=False, **kwargs):
    #     form = super(PressurePlugin, self).get_form(request, obj, change, **kwargs)

    #     qs = Widget.objects.on_site(request=request).filter(kind="pressure")

    #     choices = list(
    #         map(lambda x: (x.id, f"{x.block.mobilization.name} {x.kind} {x.id}"), qs)
    #     )

    #     form.base_fields["widget"].widget.choices = choices

    #     return form

    def render(self, context, instance, placeholder):
        context = super(PressurePlugin, self).render(context, instance, placeholder)
        context.update({"form": PressureForm()})
        return context
