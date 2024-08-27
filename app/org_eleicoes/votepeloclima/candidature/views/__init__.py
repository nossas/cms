from django.shortcuts import get_object_or_404, render
from django.views import View
from django.db.models import Q
from django.views.generic import ListView

from ..models import CandidatureFlowStatus, Candidature
from ..forms import CandidatureSearchSideForm, CandidatureSearchTopForm, ProposeForm

from ..models import CandidatureFlowStatus, Candidature
from ..forms import ProposeForm


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


class CandidatureSearchView(ListView, ProposesMixin):
    model = Candidature
    template_name = "candidature/candidature_search.html"
    context_object_name = "candidatures"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(candidatureflow__status__in=[CandidatureFlowStatus.is_valid, CandidatureFlowStatus.editing])

        form_top = CandidatureSearchTopForm(self.request.GET or None)
        form_side = CandidatureSearchSideForm(self.request.GET or None)

        if form_top.is_valid() and form_side.is_valid():
            cleaned_data = {**form_top.cleaned_data, **form_side.cleaned_data}

            for field in ['state', 'city', 'intended_position', 'political_party', 'gender', 'color', 'sexuality', 'ballot_name']:
                values = cleaned_data.get(field)
                if values:
                    if isinstance(values, list):
                        queryset = queryset.filter(**{f"{field}__in": values})
                    else:
                        queryset = queryset.filter(**{field: values})
            
            keyword = self.request.GET.get('keyword')
            if keyword:
                queryset = queryset.filter(
                    Q(short_description__icontains=keyword) |
                    Q(milestones__icontains=keyword) |
                    Q(proposes__icontains=keyword) |
                    Q(appointments__icontains=keyword)
                )
            
            is_collective_mandate = self.request.GET.get('is_collective_mandate')
            if is_collective_mandate:
                queryset = queryset.filter(is_collective_mandate=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form_top = CandidatureSearchTopForm(self.request.GET or None)
        form_side = CandidatureSearchSideForm(self.request.GET or None)

        # Atualizar as cidades com base no estado selecionado
        state = self.request.GET.get('state')
        if state:
            form_top.update_city_choices(state)

        context['form_top'] = form_top
        context['form_side'] = form_side
        
        candidature = self.get_queryset().first()
        if candidature:
            context['proposes'] = self.get_proposes(candidature)

        return context


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
