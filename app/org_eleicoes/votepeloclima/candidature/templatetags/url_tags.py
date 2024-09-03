from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()
    for key in kwargs.keys():
        if key in query:
            del(query[key])
    query.update(kwargs)
    return query.urlencode()