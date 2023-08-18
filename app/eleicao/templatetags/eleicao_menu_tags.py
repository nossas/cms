from django import template
from cms.models.pagemodel import Page

register = template.Library()


@register.inclusion_tag("eleicao/templatetags/menu.html")
def show_menu(request, classnames):
    is_draft = request.GET.get("edit") != None
    pages = Page.objects.filter(
        publisher_is_draft=is_draft,
        in_navigation=True,
    ).published(site=request.current_site)

    return {"menu": pages, "classnames": classnames}
