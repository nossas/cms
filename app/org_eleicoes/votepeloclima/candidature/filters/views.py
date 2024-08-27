from django.db.models import Q
from django.views.generic import ListView

from ..models import CandidatureFlowStatus, Candidature
# from ..forms import CandidatureSearchSideForm, CandidatureSearchTopForm

from .forms import FilterFactoryForm


class CandidatureSearchView(ListView):
    model = Candidature
    template_name = "candidature/candidature_search.html"
    context_object_name = "candidatures"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(candidatureflow__status__in=[CandidatureFlowStatus.is_valid, CandidatureFlowStatus.editing])

        form = FilterFactoryForm(data=self.request.GET or None)

        if form.is_valid():
            cleaned_data = form.cleaned_data

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

        form = FilterFactoryForm(data=self.request.GET or None)
        context.update({"form": form})

        return context


    #     form_top = CandidatureSearchTopForm(self.request.GET or None)
    #     form_side = CandidatureSearchSideForm(self.request.GET or None)

    #     # Atualizar as cidades com base no estado selecionado
    #     state = self.request.GET.get('state')
    #     if state:
    #         form_top.update_city_choices(state)

    #     context['form_top'] = form_top
    #     context['form_side'] = form_side
        
    #     candidature = self.get_queryset().first()
    #     if candidature:
    #         context['proposes'] = self.get_proposes(candidature)

    #     return context