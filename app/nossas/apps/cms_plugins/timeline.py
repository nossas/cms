from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from ..models.timeline import TimelineEvent


@plugin_pool.register_plugin
class TimelinePlugin(CMSPluginBase):
    name = "Linha do Tempo"
    module = "NOSSAS"
    render_template = "nossas/timeline/plugins/timeline_plugin.html"

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        events_world = TimelineEvent.on_site.filter(event_context="mundo")
        events_nossas = TimelineEvent.on_site.filter(event_context="nossas")

        context.update({
            "events_world": events_world,
            "events_nossas": events_nossas
        })

        return context
