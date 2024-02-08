from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from ..models.teams import MemberGroup


@plugin_pool.register_plugin
class TeamAccordionPlugin(CMSPluginBase):
    name = "Acordeão de Equipe"
    module = "NOSSAS"
    render_template = "plugins/team_accordion_plugin.html"

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        context.update({"membergroup_list": MemberGroup.on_site.all()})

        return context
