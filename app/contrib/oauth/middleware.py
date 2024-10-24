from django.http import Http404
from django.http.response import JsonResponse
from django.contrib.auth.models import User


class NoDjangoAdminForEndUserMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path.startswith("/admin/"):
            if request.user.is_authenticated and not request.user.is_staff:
                raise Http404()

        response = self.get_response(request)

        return response


class TokenAuthMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.headers.get('Authorization')

        if token:
            try:
                token_key = token.split()[1]
                request.user = User.objects.get(auth_token__key=token_key)
            except (IndexError, User.DoesNotExist):
                return JsonResponse({"detail": "Invalid token", "status_code": 401}, status=401)
        
        response = self.get_response(request)
        return response