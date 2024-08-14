from django.contrib.auth.models import User

from .base import CandidatureBaseView


class CreateCandidatureView(CandidatureBaseView):
    
    def get_current_user(self):
        data = self.get_cleaned_data_for_step("informacoes-pessoais")

        if data:
            return User.objects.get(email=data["properties"]["email"])
        elif isinstance(self.request.user, User):
            # Quando o storage perde a referência dos dados
            return self.request.user