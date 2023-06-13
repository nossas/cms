import random
import json
from typing import Any, Optional

from django.contrib import admin

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from contrib.bonde.models import Widget, ActionPressure

from .models import Pressure, TargetGroup
from .forms import PressureForm, PressureSettingsForm


class TargetGroupInline(admin.StackedInline):
    fieldset = "Alvos"
    model = TargetGroup
    template = "campaign/admin/edit_inline/stacked.html"
    extra = 1


@plugin_pool.register_plugin
class PressurePlugin(CMSPluginBase):
    name = "Pressão"
    render_template = "campaign/plugins/pressure.html"
    change_form_template = "campaign/admin/change_form.html"
    model = Pressure
    form = PressureSettingsForm
    inlines = [
        TargetGroupInline,
    ]
    fieldsets = [
        (
            "Alvos",
            {
                "fields": [
                    "widget",
                ],
                "classes": ["tab-active"],
            },
        ),
        ("Email", {"fields": ["email_subject", "email_body", "disable_editing"]}),
        ("Envio", {"fields": ["submissions_limit", "submissions_interval"]}),
        (
            "Agradecimento",
            {
                "fields": [
                    "thank_email_subject",
                    "sender_name",
                    "sender_email",
                    "thank_email_body",
                ]
            },
        ),
        ("Pós-ação", {"fields": ["sharing", "whatsapp_text"]}),
    ]

    def get_form(self, request, obj, change, **kwargs):
        form = super(PressurePlugin, self).get_form(request, obj, change, **kwargs)

        widget_field = form.base_fields.get("widget", None)
        if widget_field:
            widget_field.widget.choices = list(
                map(
                    lambda x: (x.id, f"{x.block.mobilization.name} {x.kind} #{x.id}"),
                    Widget.objects.on_site(request).filter(kind="pressure"),
                )
            )
            form.base_fields["widget"] = widget_field

        return form

    def render(self, context, instance, placeholder):
        context = super(PressurePlugin, self).render(context, instance, placeholder)
        request = context["request"]
        initial = dict()

        if instance:
            initial["instance"] = instance.id
            initial["email_subject"] = random.choice(json.loads(instance.email_subject))
            initial["email_body"] = instance.email_body

        if request.method == "POST":
            form = PressureForm(request.POST, initial=initial)

            if form.is_valid():
                form.submit()
        else:
            form = PressureForm(initial=initial)

        size = 0
        if hasattr(instance, "widget"):
            size = (
                # Garante apenas pessoas que pressionaram
                # e não número total de pressões
                ActionPressure.objects.filter(widget=instance.widget)
                .values("activist_id")
                .distinct()
                .count()
            )

        context.update({"form": form, "size": size})
        return context
