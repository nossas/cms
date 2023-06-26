from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from contrib.bonde.models import Widget, ActionPressure

from .models import Pressure
from .forms import PressureForm, PressureSettingsForm

# Widget Settings
#
# main_color: string;
# call_to_action?: string;
# title_text: string;
# button_text: string;
# pressure_subject?: string;
# pressure_body?: string;
# disable_edit_field: string;
# targets: string;
# finish_message_type?: string;
# finish_message?: Record<any, any>;
# finish_message_background?: string;
# count_text?: string;
# show_city?: string;
# show_state?: string;
# pressure_type?: string | 'unique' | 'group';
# optimization_enabled?: boolean;


@plugin_pool.register_plugin
class PressurePlugin(CMSPluginBase):
    name = "Pressão"
    module = "Estrategia"
    render_template = "campaign/plugins/pressure.html"
    model = Pressure
    form = PressureSettingsForm

    def render(self, context, instance, placeholder):
        context = super(PressurePlugin, self).render(context, instance, placeholder)
        request = context["request"]
        initial = dict()
        settings = dict()

        if instance and instance.widget_id:
            widget = Widget.objects.get(id=instance.widget_id)
            initial["instance"] = instance.id

            # Alvos vindos do Bonde
            settings["title"] = widget.settings.get("title_text", "Envie um e-mail mandando seu recado")
            settings["button"] = widget.settings.get("button_text", "Pressionar")
            settings["count"] = widget.settings.get("count_text", "pessoas já pressionaram")
            settings["targets"] = list(
                map(
                    lambda x: dict(
                        name=x.split("<")[0],
                        email=x.split("<")[-1].replace(">", ""),
                    ),
                    widget.settings.get("targets", []),
                )
            )

            email_subject = widget.settings.get("pressure_subject", "")
            # initial["email_subject"] = random.choice(json.loads(instance.email_subject))
            initial["email_subject"] = email_subject

            email_body = widget.settings.get("pressure_body", "")
            initial["email_body"] = email_body

        if request.method == "POST":
            form = PressureForm(request.POST, initial=initial)

            if form.is_valid():
                form.submit()
        else:
            form = PressureForm(initial=initial)

        size = 0
        if hasattr(instance, "widget_id"):
            size = (
                # Garante apenas pessoas que pressionaram
                # e não número total de pressões
                ActionPressure.objects.filter(widget=instance.widget_id)
                .values("activist_id")
                .distinct()
                .count()
            )

        context.update({"form": form, "size": size, "settings": settings})
        return context
