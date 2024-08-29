from django.shortcuts import get_object_or_404, render
from django.views import View

from ..models import CandidatureFlowStatus, Candidature
from ..forms.register import ProposeForm


class ProposesMixin:
    def get_proposes(self, candidature):
        proposes_list = []

        for field_name, value in candidature.proposes.items():
            if value:
                proposes_list.append({
                    "label": ProposeForm().fields[field_name].checkbox_label,
                    "description": value
                })

        return proposes_list


class PublicCandidatureView(View, ProposesMixin):
    template_name = "candidature/candidate_profile.html"

    def get(self, request, slug):
        candidature = get_object_or_404(Candidature, slug=slug)
        context = {
            "candidature": candidature,
            "proposes": self.get_proposes(candidature),
        }

        # Verifica se a candidatura está aprovada
        if candidature.status() != CandidatureFlowStatus.is_valid.label:
            return render(request, 'candidature/not_approved.html', context)

        return render(request, self.template_name, context)
