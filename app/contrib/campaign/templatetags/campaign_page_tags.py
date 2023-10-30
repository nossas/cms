from django import template

register = template.Library()


@register.simple_tag
def get_absolute_url(request, path=""):
    return request.scheme + "://" + request.get_host() + path
