# EleicaoNavbarPlugin
from django.core.paginator import Paginator

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import Candidate, CandidateStatusChoices
from .forms.filters import CandidateListFilter


@plugin_pool.register_plugin
class EleicaoNavbarPlugin(CMSPluginBase):
    name = "Navbar"
    module = "A Eleição do Ano"
    render_template = "eleicao/plugins/navbar.html"


@plugin_pool.register_plugin
class EleicaoFooterPlugin(CMSPluginBase):
    name = "Assinatura"
    module = "A Eleição do Ano"
    render_template = "eleicao/plugins/footer.html"

@plugin_pool.register_plugin
class EleicaoCarouselPlugin(CMSPluginBase):
    name = "Carousel"
    module = "A Eleição do Ano"
    render_template = "eleicao/plugins/carousel.html"


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
