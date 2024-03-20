from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from ..models.timeline import TimelineEvent


@plugin_pool.register_plugin
class TimelinePlugin(CMSPluginBase):
    name = "Linha do Tempo"
    module = "NOSSAS"
    render_template = "nossas/timeline/plugins/timeline_plugin.html"

    # def render(self, context, instance, placeholder):
    #     context = super().render(context, instance, placeholder)

    #     context.update({"event_list": TimelineEvent.on_site.filter()})

    #     return context