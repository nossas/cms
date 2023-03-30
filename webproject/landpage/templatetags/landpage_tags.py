from copy import copy
from django import template
from django.template import loader, Context
from django.shortcuts import render

register = template.Library()


@register.simple_tag(takes_context=True)
def landpage_create_menu(context, template_name='landpage/menu.html'):
    placeholder = context['request'].current_page.placeholders.first()
    menus = list(map(
        lambda plugin: plugin.get_plugin_instance()[0],
        placeholder.get_plugins().filter(plugin_type='ContentPlugin')
    ))

    template = loader.get_template(template_name)

    # import ipdb; ipdb.set_trace()
    return template.render({ 'children': menus })