from django.db.models import Prefetch
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from ..models.teams import MemberGroup, Member


@plugin_pool.register_plugin
class TeamAccordionPlugin(CMSPluginBase):
    name = "Acordeão de Equipe"
    module = "NOSSAS"
    render_template = "plugins/team_accordion_plugin.html"

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        context.update(
            {
                "membergroup_list": MemberGroup.on_site.prefetch_related(
                    Prefetch(
                        "member_set", queryset=Member.on_site.order_by("my_order", "full_name")
                    )
                ).order_by("my_order", "id").all()
            }
        )

        return context
