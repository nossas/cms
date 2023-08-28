from typing import Any, Dict
from collections import ChainMap

from django.db import transaction
from django.db.models.query import QuerySet
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.core.files.storage import DefaultStorage
from django.utils.text import slugify
from django.http import JsonResponse


from formtools.wizard.views import SessionWizardView

from .bonde_utils import create_form_entry
from .forms.candidate import (
    IntroForm,
    Commitment1Form,
    Commitment2Form,
    PersonalInfo1Form,
    CandidatureForm,
    PersonalInfo2Form,
    PersonalInfo3Form,
)
from .forms.filters import CandidateListFilter
from .models import Candidate, CandidateStatusChoices

from urllib import parse

# Create your views here.


class CandidateListView(ListView):
    template_name = "eleicao/candidate_list.html"
    model = Candidate
    paginate_by = 10

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx["form"] = CandidateListFilter(self.request.GET)

        return ctx

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset().filter(status=CandidateStatusChoices.published)

        filter_state = self.request.GET.get("uf", None)
        if filter_state:
            return qs.filter(place__state__iexact=filter_state)

        return qs


class CandidateCreateView(SessionWizardView):
    template_name = "eleicao/candidate_wizard_form.html"
    # Ordered of form steps same this list
    form_list = [
        IntroForm,
        Commitment1Form,
        Commitment2Form,
        PersonalInfo1Form,
        CandidatureForm,
        PersonalInfo2Form,
        PersonalInfo3Form,
    ]

    file_storage = DefaultStorage()

    # model = Candidate
    # fields = "__all__"

    def process_step_files(self, form):
        return self.get_form_step_files(form)

    @transaction.atomic
    def done(self, form_list, **kwargs):
        values = list(map(lambda form: form.cleaned_data, form_list))
        values = dict(ChainMap(*values))

        # Processar os valores
        values.pop("agree")
        values.pop("agree_2")
        values.pop("agree_3")
        values.pop("agree_4")
        values.pop("agree_5")
        values.pop("agree_6")
        values.pop("agree_7")
        values.pop("agree_8")
        values.pop("agree_9")
        values.pop("agree_10")
        values.pop("agree_11")
        values.pop("agree_12")

        # PollingPlace
        state = values.pop("state")
        city = values.pop("city")
        place_id = values.pop("place")

        values["place_id"] = int(place_id)

        photo = values.pop("photo")
        video = values.pop("video")

        obj = Candidate.objects.create(**values, photo=photo, video=video)
                      
        obj.save()

        # Integrate with Bonde
        settings = {
            "widget_id": 76494,
            "mobilization_id": 7302,
            "cached_community_id": 263,
        }

        fe = create_form_entry(settings=settings, state=state, city=city, **values)

        print(fe)

        return redirect(obj.get_absolute_url() + "?modal=true")


class CandidateDetailView(DetailView):
    template_name = "eleicao/candidate_detail.html"
    model = Candidate

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        modal = self.request.GET.get("modal")
        candidate = self.object
        if modal:
            msg_whatsapp_modal = parse.quote(
                "Olá! Eu me candidatei ao Conselho Tutelar em minha cidade e agora faço parte da plataforma A Eleição do Ano, criada para impulsionar candidaturas alinhadas com o Estatuto da Criança e do Adolescente. Tenho um perfil na plataforma apresentando um pouco sobre mim! Vem conhecer: "
                + "\n"
                + self.request.build_absolute_uri().replace("/?modal=true", "")
            )
            msg_twitter_modal = parse.quote(
                "Me candidatei ao Conselho Tutelar em minha cidade e agora faço parte da plataforma A Eleição do Ano, criada para impulsionar candidaturas alinhadas com o Estatuto da Criança e do Adolescente. Tenho um perfil na plataforma, vem conhecer: "
                + self.request.build_absolute_uri().replace("/?modal=true", "")
            )
            ctx.update(
                {
                    "modal_is_open": True,
                    "msg_whatsapp_modal": msg_whatsapp_modal,
                    "msg_twitter_modal": msg_twitter_modal,
                }
            )

        msg_whatsapp = parse.quote(
            f"Oie! Tá sabendo da Eleição do Ano? Sim, esse ano temos uma eleição importantíssima: os municípios brasileiros vão eleger conselheiros e conselheiras tutelares no dia 1 de outubro. É o futuro das nossas crianças e adolescentes em jogo! Não fique de fora, conheça {candidate.name}"
            + "\n"
            + self.request.build_absolute_uri()
        )
        msg_twitter = parse.quote(
            f"A Eleição do Ano está chegando! É hora de votar pelo futuro das crianças. Conheça {candidate.name} "
            + self.request.build_absolute_uri()
        )
        msg_copy_link = parse.quote(self.request.build_absolute_uri())

        ctx.update(
            {
                "msg_whatsapp": msg_whatsapp,
                "msg_twitter": msg_twitter,
                "msg_copy_link": msg_copy_link,
            }
        )
        return ctx

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(status=CandidateStatusChoices.published)


class ResultsCandidateView(ListView):
    template_name = "eleicao/voter_results.html"
    model = Candidate

    def get_queryset(self) -> QuerySet[Any]:
        qs = Candidate.objects.filter(status=CandidateStatusChoices.published)

        filter_state = self.request.GET.get("uf", None)
        filter_zone = self.request.GET.get("zone", None)
        if filter_state:
            return qs.filter(state__iexact=filter_state)
        if filter_zone:
            return qs.filter(zone=filter_zone)

        return qs


# Sugerir uma slug
def suggest_slug(request):
    name = request.GET.get("name")    
    slug = slugify(name).replace("-", "")
    suggestion = slug
    list_candidate = Candidate.objects.filter(slug=slug)
    total = list_candidate.count()
    sufix = 1
    while total > 0:
        suggestion = slug + f"{sufix}"
        list_candidate = Candidate.objects.filter(slug=suggestion)
        total = list_candidate.count()
        sufix = sufix + 1

    return JsonResponse({"slug": suggestion})
