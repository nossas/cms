from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm


class OAuthPasswordResetForm(PasswordResetForm):

    def get_users(self, email):
        users = User.objects.filter(**{
            "is_staff": False,
            "is_superuser": False,
            "email__iexact": email
        })
        return users