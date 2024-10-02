from django import template
from django.conf import settings
# from django.conf import settings
# from django.utils.text import slugify
from django.utils.safestring import mark_safe

from cms.models.placeholdermodel import Placeholder

register = template.Library()


@register.simple_tag
def render_slider_navigation(slotname, language=settings.LANGUAGE_CODE):
    # request = context["request"]
    plugins = Placeholder.objects.filter(slot=slotname).first().get_child_plugins(
        language=language
    )

    html = ""

    for i, plugin in enumerate(plugins):
        classname = ' class="active"' if i == 0 else ''
        html += f'<button type="button" data-bs-target="#sliderFullIndicators" data-bs-slide-to="{i}"{classname} aria-current="true" aria-label="Slide {i+1}"></button>'

    return mark_safe(html)
