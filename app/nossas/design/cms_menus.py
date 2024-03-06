from menus.base import Modifier
from menus.menu_pool import menu_pool
from cms.models import Page


class I18nModifier(Modifier):
    """
    This modifier makes the i18n_title attribute of a page
    accessible for the menu system
    """

    def modify(self, request, nodes, namespace, root_id, post_cut, breadcrumb):
        if post_cut:
            page_nodes = {n.id: n for n in nodes if n.attr["is_page"]}

            pages = Page.objects.filter(id__in=page_nodes.keys())
            exclude_nodes = []
            for page in pages:
                if request.LANGUAGE_CODE in page.get_languages():
                    node = page_nodes[page.id]
                    node.attr["i18n_menu_title"] = page.get_menu_title()

                    if len(node.children) > 0:
                        node.children = self.modify(
                            request,
                            node.children,
                            namespace,
                            root_id,
                            post_cut,
                            breadcrumb,
                        )
                else:
                    exclude_nodes.append(page.id)

            nodes = list(filter(lambda x: x.id not in exclude_nodes, nodes))

        return nodes


menu_pool.register_modifier(I18nModifier)
