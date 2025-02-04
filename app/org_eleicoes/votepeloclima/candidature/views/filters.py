from django.db.models import Q
from django.views.generic import ListView

from ..models import CandidatureFlowStatus, Candidature
from ..forms.filters import FilterFactoryForm
from ..choices import ElectionStatus


class CandidatureSearchView(ListView):
    model = Candidature
    template_name = "candidature/candidature_search.html"
    context_object_name = "candidatures"
    paginate_by = 12

    search_filter_fields = [
        "legal_name",
        "ballot_name",
        "proposes",
        "milestones",
        "short_description",
    ]
    unique_filter_fields = ["political_party", "state", "city", "intended_position"]
    multiple_filter_fields = ["gender", "color", "proposes", "sexuality"]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Retorna apenas Candidaturas que já tiveram status valido em algum momento do preenchimento
        queryset = queryset.filter(
            candidatureflow__status__in=[
                CandidatureFlowStatus.is_valid,
                CandidatureFlowStatus.editing,
            ]
        )

        # Filtra por valores selecionado pelo usuário
        form = FilterFactoryForm(data=self.request.GET or None)

        if form.is_valid():
            cleaned_data = form.cleaned_data

            # Filtros AND
            for field_name in self.unique_filter_fields:
                value = cleaned_data.get(field_name)
                if value:
                    queryset = queryset.filter(**{field_name: value})

            # Filters OR with Text search ICONTAINS
            query = Q()
            for field_name in self.search_filter_fields:
                value = cleaned_data.get("keyword")
                if value:
                    query |= Q(**{f"{field_name}__icontains": value})

            queryset = queryset.filter(query)

            self.multiple_filter_fields

            # Filters OR with Multiple Choice
            for field_name in self.multiple_filter_fields:
                query = Q()
                values = cleaned_data.get(field_name)
                for value in values:
                    if field_name == "proposes":
                        query |= ~Q(**{f"{field_name}__{value}__exact": ""})
                    else:
                        query |= Q(**{f"{field_name}__exact": value})

                # Filter is concatenate with AND by field multiple value
                queryset = queryset.filter(query)

            # Filtra apenas mandato coletivo
            mandate_type = self.request.GET.get("mandate_type")
            if mandate_type:
                queryset = queryset.filter(
                    is_collective_mandate=(
                        True if mandate_type == "coletivo" else False
                    )
                )

            election_status = cleaned_data.get("election_status", "elected")
        else:
            election_status = "elected"
        
        # Filtra com base no status da eleição
        if election_status == "second_round":
            # Filtra candidaturas que foram para o 2º turno
            queryset = queryset.filter(election_results__status=ElectionStatus.segundo_turno)
        elif election_status == "elected":
            # Filtra candidaturas eleitas
            queryset = queryset.filter(election_results__status=ElectionStatus.eleita)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = FilterFactoryForm(data=self.request.GET or None)
        context.update({"form": form})

        return context
