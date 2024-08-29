from django.views import View
from django.http import JsonResponse

from ..locations_utils import get_choices


class AddressView(View):

    def get(self, request, *args, **kwargs):
        state = request.GET.get("state")
        cities = get_choices(state)
        return JsonResponse([{'code': code, 'name': name} for code, name in cities], safe=False)