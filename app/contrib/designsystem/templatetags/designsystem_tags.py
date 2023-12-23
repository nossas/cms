from django import template

register = template.Library()


@register.filter
def update_class_attributes(value, arg=None):
    # TODO: process better this value
    if arg:
        return value.replace('collapse"', f'collapse {arg}"').replace('collapsed"', f'collapsed {arg}"')

    return value
