from django.contrib import admin

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from contrib.bonde.models import Widget

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
    # model = Dummy
    form = PressureSettingsForm
    inlines = [
        TargetGroupInline,
    ]
    fieldsets = [
        ("Alvos", {"fields": [], "classes": ["tab-active"]}),
        ("Email", {"fields": ["email_subject", "email_body", "disable_editing"]}),
        ("Envio", {"fields": ["submissions_limit", "submissions_interval"]}),
        ("Agradecimento", {"fields": ["thank_email_subject", "sender_name", "sender_email", "thank_email_body"]}),
        ("Pós-ação", {"fields": ["sharing", "whatsapp_text"]})
    ]
    # fieldsets = [
    # ("Alvos", {"fields": ["is_group", "email_subject"], "classes": ["tab-active"]}),
    # ("Email", {"fields": ["disable_editing"]}),
    # (
    #     "Envio",
    #     {
    #         "fields": ["submissions_limit", "submissions_interval"],
    #     },
    # ),
    # (
    #     "Agradecimento",
    #     {
    #         "fields": [
    #             "email_subject",
    #             "sender_name",
    #             "sender_email",
    #             "email_body",
    #         ],
    #     },
    # ),
    # ("Pós-ação", {"fields": ["sharing", "whatsapp_text"]}),
    # ]

    # return super().save_form(request, form, change)

    # def get_form(self, request, obj=None, change=False, **kwargs):
    #     form = super(PressurePlugin, self).get_form(request, obj, change, **kwargs)

    #     qs = Widget.objects.on_site(request=request).filter(kind="pressure")

    #     choices = list(
    #         map(lambda x: (x.id, f"{x.block.mobilization.name} {x.kind} {x.id}"), qs)
    #     )

    #     form.base_fields["widget"].widget.choices = choices

    #     return form

    def render_change_form(
        self, request, context, add=False, change=False, form_url="", obj=None
    ):
        sorted_inline_formsets = {}
        inline_admin_formsets = context["inline_admin_formsets"]
        formsets_to_remove = []

        for inline_formset in inline_admin_formsets:
            if hasattr(inline_formset.opts, "fieldset"):
                fieldset = inline_formset.opts.fieldset
                if fieldset in sorted_inline_formsets:
                    sorted_inline_formsets[fieldset].append(inline_formset)
                else:
                    sorted_inline_formsets.update(
                        {
                            fieldset: [
                                inline_formset,
                            ]
                        }
                    )
                formsets_to_remove.append(inline_formset)

        for inline_formset in formsets_to_remove:
            inline_admin_formsets.remove(inline_formset)

        context.update(
            {
                "sorted_inline_formsets": sorted_inline_formsets,
                "inline_admin_formsets": inline_admin_formsets,
            }
        )

        # import ipdb;ipdb.set_trace()
        return super(PressurePlugin, self).render_change_form(
            request, context, add, change, form_url, obj
        )

    def render(self, context, instance, placeholder):
        context = super(PressurePlugin, self).render(context, instance, placeholder)
        context.update({"form": PressureForm()})
        return context
