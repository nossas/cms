# EleicaoNavbarPlugin
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

    def render(self, context, instance, placeholder):
        ctx = super().render(context, instance, placeholder)
        request = ctx.get("request")

        ctx["form"] = CandidateListFilter(request.GET)
        # Filtered List
        ctx["object_list"] = Candidate.objects.filter(
            status=CandidateStatusChoices.published
        )

        filter_state = request.GET.get("uf", None)
        if filter_state:
            ctx["object_list"] = ctx["object_list"].filter(
                place__state__iexact=filter_state
            )

        return ctx
