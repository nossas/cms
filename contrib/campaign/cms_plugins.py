from typing import Any, Optional
from django.db.models import Q

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from contrib.bonde.models import Widget

from .models import Pressure
from .forms import PressureForm, PressureSettingsForm


@plugin_pool.register_plugin
class PressurePlugin(CMSPluginBase):
    name = "Pressão"
    render_template = "campaign/plugins/pressure.html"
    model = Pressure
    form = PressureSettingsForm

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(PressurePlugin, self).get_form(request, obj, change, **kwargs)
        
        qs = Widget.objects.on_site(request=request).filter(kind='pressure')
        
        choices = list(map(lambda x: (x.id, f'{x.block.mobilization.name} {x.kind} {x.id}'), qs))

        form.base_fields['widget'].widget.choices = choices

        return form

    def render(self, context, instance, placeholder):
        context = super(PressurePlugin, self).render(context, instance, placeholder)
        context.update({"form": PressureForm()})
        return context