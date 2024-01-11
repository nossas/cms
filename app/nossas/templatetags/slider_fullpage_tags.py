from django import template
# from django.conf import settings
# from django.utils.text import slugify
from django.utils.safestring import mark_safe

from cms.models.placeholdermodel import Placeholder

register = template.Library()


@register.simple_tag(takes_context=True)
def render_slider_navigation(context):
    request = context["request"]
    plugins = Placeholder.objects.filter(slot="nossas_home_content").first().get_child_plugins(
        language=request.LANGUAGE_CODE
    )

    html = ""

    for i, plugin in enumerate(plugins):
        classname = ' class="active"' if i == 0 else ''
        html += f'<button type="button" data-bs-target="#sliderFullIndicators" data-bs-slide-to="{i}"{classname} aria-current="true" aria-label="Slide {i+1}"></button>'

    return mark_safe(html)
