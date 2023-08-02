from django.http import JsonResponse

from ..models import PollingPlace
from ..csv.choices import get_choices


def fetch_cep(request):
    state = request.GET.get("state")
    city = request.GET.get("city")
    neighborhood = request.GET.get("neighborhood")

    if not neighborhood:
        choices = get_choices(state, city)
    else:
        qs = PollingPlace.objects.filter(
            places__state=state, places__city=city, places__neighborhood=neighborhood
        ).values_list("id", "name")

        choices = list(map(lambda x: x, qs))

    return JsonResponse({"choices": choices})

