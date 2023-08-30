import re
from django import template

register = template.Library()


@register.inclusion_tag("eleicao/templatetags/candidate_list.html")
def render_candidate_list(voter):
    return {}