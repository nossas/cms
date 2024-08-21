from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.views import View

from formtools.wizard.views import NamedUrlSessionWizardView

from ..models import CandidatureFlowStatus, Candidature
from ..forms import ProposeForm
from ..locations_utils import get_choices


class AddressView(View):
    def get(self, request, *args, **kwargs):
        state = request.GET.get("state")
        cities = get_choices(state)

        return JsonResponse([{'code': code, 'name': name} for code, name in cities], safe=False)


class PublicCandidatureView(View):
    template_name = "candidature/candidate_profile.html"

    def get(self, request, slug):
        candidature = get_object_or_404(Candidature, slug=slug)
        proposes_list = []

        for field_name, value in candidature.proposes.items():
            if value:
                proposes_list.append({
                    "label": ProposeForm().fields[field_name].checkbox_label,
                    "description": value
                })

        context = {
            "candidature": candidature,
            "proposes": proposes_list,
        }

        # Verifica se a candidatura está aprovada
        if candidature.status() != CandidatureFlowStatus.is_valid.label:
            return render(request, 'candidature/not_approved.html', context)
        
        return render(request, self.template_name, context)