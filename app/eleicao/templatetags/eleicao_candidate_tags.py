import re
from django import template

from ..models import Voter, Candidate
from ..forms.create import VoterForm

from urllib import parse


register = template.Library()


@register.inclusion_tag("eleicao/templatetags/candidate_list.html")
def render_candidate_list(voter: Voter, request=None, instance=None, placeholder=None):
    form = VoterForm(data=request.POST)

    object_list = None

    if form.is_valid():
        if not voter.place and not voter.city:
            object_list = Candidate.objects.filter(
                place__state=form.cleaned_data.get("state")
            )
        elif not voter.place:
            object_list = Candidate.objects.filter(
                place__state=form.cleaned_data.get("state"),
                place__city=form.cleaned_data.get("city")
            )
        else:
            object_list = Candidate.objects.filter(place=form.cleaned_data.get("place"))

    url = "https://aeleicaodoano.org"

    msg_whatsapp = parse.quote(
        f"Oie! Tá sabendo da Eleição do Ano? Sim, esse ano temos uma eleição importantíssima: os municípios brasileiros vão eleger conselheiros e conselheiras tutelares no dia 1 de outubro. É o futuro das nossas crianças e adolescentes em jogo! Não fique de fora:"
        + "\n"
        + url
    )
    msg_twitter = parse.quote(
        f"Acabei de me comprometer a participar da Eleição do Ano, que define o presente e o futuro do nosso país no dia 1 de outubro. Vem você também defender nossas crianças e adolescentes: "
        + url
    )
    url_facebook_modal = parse.quote(url + "&amp;src=sdkpreparse")
    msg_copy_link = url

    return {
        "object_list": object_list,
        "is_empty": not object_list.exists(),
        "msg_whatsapp": msg_whatsapp,
        "msg_twitter": msg_twitter,
        "url_facebook_modal": url_facebook_modal,
        "msg_copy_link": msg_copy_link,
        "form": form,
    }
