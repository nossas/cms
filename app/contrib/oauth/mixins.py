from django.http import JsonResponse
from django.contrib.auth.mixins import AccessMixin


class JsonLoginRequiredMixin(AccessMixin):
    """Mixin que verifica se o usuário está autenticado e retorna um JSON 401 se não estiver."""
    
    def handle_no_permission(self):
        return JsonResponse({"detail": "Invalid token", "status_code": 401}, status=401)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        return super().dispatch(request, *args, **kwargs)