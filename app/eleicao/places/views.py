from django.http import JsonResponse

from ..models import PollingPlace


# Busca as opções pelos endereços cadastrados
def get_choices(uf, city=None):
    choices = []
    if city:
        list_address = PollingPlace.objects.filter(state=uf, city=city)
    else:
        list_address = PollingPlace.objects.filter(state=uf)

    for address in list_address:
        if city:
            choices.append((address.name, address.name.title()))
        else:
            choices.append((address.city, address.city.title()))

    return list(set(choices))


def fetch_cep(request):
    state = request.GET.get("state")
    city = request.GET.get("city")
    # name = request.GET.get("name")

    if state and city:
        qs = PollingPlace.objects.filter(
            state=state, city=city
        ).values_list("id", "place")

        choices = list(map(lambda x: x, qs))
    else:
        choices = get_choices(state, city)

    return JsonResponse({"choices": choices})
