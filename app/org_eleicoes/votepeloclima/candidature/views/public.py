from django.http import JsonResponse
from django.views import View
from django.views.generic.detail import DetailView

from ..models import CandidatureFlowStatus, Candidature
from ..locations_utils import get_choices


class AddressView(View):

    def get(self, request, *args, **kwargs):
        state = request.GET.get("state")
        cities = get_choices(state)
        return JsonResponse(
            [{"code": code, "name": name} for code, name in cities], safe=False
        )


class PublicCandidatureView(DetailView):
    model = Candidature
    template_name = "candidature/candidate_profile.html"

    def get_queryset(self):
        qs = super().get_queryset()
        # Retorna apenas Candidaturas que já tiveram status valido em algum momento do preenchimento
        qs = qs.filter(
            candidatureflow__status__in=[
                CandidatureFlowStatus.is_valid,
                CandidatureFlowStatus.editing,
            ]
        )
        return qs
