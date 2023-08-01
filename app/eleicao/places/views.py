from django.http import JsonResponse
from ..csv.choices import get_choices


def fetch_cep(request):
    state = request.GET.get("state")
    city = request.GET.get("city")
    choices = get_choices(state,city)
    return JsonResponse({"choices": choices})


# def fetch_cities(request, uf):
#     return JsonResponse({"choices": [{"value": "", "label": ""}]})


# def fetch_neighborhoods(request, city):
#     return JsonResponse({"choices": [{"value": "", "label": ""}]})
