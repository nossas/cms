from django.http import JsonResponse

from ..models import PollingPlace, Address


# Busca as opções pelos endereços cadastrados
def get_choices(uf, city=None):
    choices = []
    if city:
        list_address = Address.objects.filter(state=uf, city=city)
    else:
        list_address = Address.objects.filter(state=uf)

    for address in list_address:
        if address.state == uf:
            if city:
                if city == address.city:
                    choices.append(
                        (address.neighborhood, address.neighborhood.capitalize())
                    )
            else:
                choices.append((address.city, address.city.capitalize()))

    return list(set(choices))


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
