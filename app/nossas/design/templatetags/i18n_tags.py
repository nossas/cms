from django import template
from django.conf import settings
from django.utils.text import slugify
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def get_i18n_menu_title(child):
    from cms.models import Page

    page = Page.objects.get(id=child.id)

    return page.get_menu_title()