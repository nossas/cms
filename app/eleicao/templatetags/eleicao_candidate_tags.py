import re
from django import template

from ..models import Voter, Candidate


register = template.Library()


@register.inclusion_tag("eleicao/templatetags/candidate_list.html")
def render_candidate_list(voter: Voter):
    object_list = Candidate.objects.filter(place__state=voter.state, place__city=voter.city)

    return {
        "object_list": object_list
    }
