import re
from django import template

from ..models import Voter, Candidate


register = template.Library()


@register.inclusion_tag("eleicao/templatetags/candidate_list.html")
def render_candidate_list(voter: Voter):
    if not voter.place:
        object_list = Candidate.objects.filter(
            place__state=voter.state, place__city=voter.city
        )
    else:
        object_list = Candidate.objects.filter(place=voter.place)

    return {"object_list": object_list}
