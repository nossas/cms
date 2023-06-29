from django import template
from django.db.models import Q

from classytags.arguments import StringArgument
from classytags.core import Options
from classytags.helpers import InclusionTag


register = template.Library()


class ShowMenu(InclusionTag):
    """
    render a nested list of all children of the pages
    - from_level: starting level
    - to_level: max level
    - extra_inactive: how many levels should be rendered of the not active tree?
    - extra_active: how deep should the children of the active node be rendered?
    - namespace: the namespace of the menu. if empty will use all namespaces
    - root_id: the id of the root node
    - template: template used to render the menu
    """
    name = 'show_menu'
    template = 'menu/dummy.html'

    options = Options(
        # IntegerArgument('from_level', default=0, required=False),
        # IntegerArgument('to_level', default=100, required=False),
        # IntegerArgument('extra_inactive', default=0, required=False),
        # IntegerArgument('extra_active', default=1000, required=False),
        StringArgument('template', default='menu/menu.html', required=False),
        # StringArgument('namespace', default=None, required=False),
        # StringArgument('root_id', default=None, required=False),
        # Argument('next_page', default=None, required=False),
    )

    def get_context(self, context, template):
        current_page = context['request'].current_page

        current_page = context["request"].current_page

        placeholder = current_page.get_placeholders().first()

        if placeholder:
            plugins = placeholder.get_child_plugins().filter(
                Q(plugin_type="BlockPlugin") | Q(plugin_type="GridBlockPlugin")
            )

            context['template'] = template
            
            context["children"] = list(filter(lambda x: not x.menu_hidden, map(lambda x: x.get_bound_plugin(), plugins)))
        else:
            context["template"] = template

            context["children"] = list()

        # try:
        #     # If there's an exception (500), default context_processors may not be called.
        #     request = context['request']
        # except KeyError:
        #     return {'template': 'menu/empty.html'}

        # if next_page:
        #     children = next_page.children
        # else:
        #     # new menu... get all the data so we can save a lot of queries
        #     menu_renderer = context.get('cms_menu_renderer')

        #     if not menu_renderer:
        #         menu_renderer = menu_pool.get_renderer(request)

        #     nodes = menu_renderer.get_nodes(namespace, root_id)
        #     if root_id:  # find the root id and cut the nodes
        #         id_nodes = menu_pool.get_nodes_by_attribute(nodes, "reverse_id", root_id)
        #         if id_nodes:
        #             node = id_nodes[0]
        #             nodes = node.children
        #             for remove_parent in nodes:
        #                 remove_parent.parent = None
        #             from_level += node.level + 1
        #             to_level += node.level + 1
        #             nodes = flatten(nodes)
        #         else:
        #             nodes = []
        #     children = cut_levels(nodes, from_level, to_level, extra_inactive, extra_active)
        #     children = menu_renderer.apply_modifiers(children, namespace, root_id, post_cut=True)

        # context['children'] = children
        # context['template'] = template
        # context['from_level'] = from_level
        # context['to_level'] = to_level
        # context['extra_inactive'] = extra_inactive
        # context['extra_active'] = extra_active
        # context['namespace'] = namespace

        return context


register.tag("show_menu", ShowMenu)