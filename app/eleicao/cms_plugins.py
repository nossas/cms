# EleicaoNavbarPlugin
from django.core.paginator import Paginator

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .bonde_utils import create_form_entry

from .models import Candidate, CandidateStatusChoices, EleicaoCarousel
from .forms.filters import CandidateListFilter
from .forms.create import VoterForm


@plugin_pool.register_plugin
class EleicaoNavbarPlugin(CMSPluginBase):
    name = "Navbar"
    module = "A Eleição do Ano"
    render_template = "eleicao/plugins/navbar.html"
    allow_children = False


@plugin_pool.register_plugin
class EleicaoFooterPlugin(CMSPluginBase):
    name = "Assinatura"
    module = "A Eleição do Ano"
    render_template = "eleicao/plugins/footer.html"


@plugin_pool.register_plugin
class EleicaoCarouselPlugin(CMSPluginBase):
    name = "Carousel"
    model = EleicaoCarousel
    module = "A Eleição do Ano"
    render_template = "eleicao/plugins/carousel.html"

    def render(self, context, instance, placeholder):
        ctx = super().render(context, instance, placeholder)
        ctx.update({"title": instance.title, "description": instance.description})
        return ctx


@plugin_pool.register_plugin
class EleicaoCandidateListPlugin(CMSPluginBase):
    name = "Lista de candidaturas"
    module = "A Eleição do Ano"
    render_template = "eleicao/plugins/candidate_list.html"
    per_page = 5

    def render(self, context, instance, placeholder):
        ctx = super().render(context, instance, placeholder)
        request = ctx.get("request")

        ctx["form"] = CandidateListFilter(request.GET)

        # Filtered List
        qs = Candidate.objects.filter(status=CandidateStatusChoices.published)
        filter_state = request.GET.get("uf", None)
        if filter_state:
            qs = qs.filter(place__state__iexact=filter_state)

        page_number = request.GET.get("page", 1)
        p = Paginator(qs, self.per_page)
        page_obj = p.get_page(page_number)

        ctx["paginator"] = p
        ctx["is_paginated"] = p.count > 1
        ctx["page_obj"] = page_obj
        ctx["object_list"] = page_obj.object_list

        return ctx


@plugin_pool.register_plugin
class EleicaoVoterFormPlugin(CMSPluginBase):
    name = "Formulário de Eleitor(a)"
    module = "A Eleição do Ano"
    render_template = "eleicao/plugins/voter_form.html"

    def render(self, context, instance, placeholder):
        ctx = super().render(context, instance, placeholder)
        request = ctx.get("request")

        ctx["form"] = VoterForm()

        if request.method == "POST":
            form = VoterForm(request.POST)

            if form.is_valid():
                instance = form.save(commit=True)
                
                settings = {
                    "widget_id": 76616,
                    "mobilization_id": 7302,
                    "cached_community_id": 263,
                }

                fe = create_form_entry(settings=settings, **form.cleaned_data)

                print(fe)
                ctx["success"] = True

            ctx["form"] = form

        return ctx
