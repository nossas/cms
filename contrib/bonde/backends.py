import bcrypt

from django.contrib.auth.models import Group
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from .models import User as UserBonde


class BondeBackend(ModelBackend):
    """
    Cria um novo usuário caso ele exista no Bonde e adiciona ao
    grupo Mobilizador se esse usuário não for administrador.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super(BondeBackend, self).authenticate(
            request, username, password, **kwargs
        )

        # Se usuário ainda não existir na plataforma, buscamos na base de dados do Bonde
        if not user:
            user_bonde = UserBonde.objects.get(email=username)

            if user_bonde and bcrypt.checkpw(
                bytes(password, "utf-8"), bytes(user_bonde.encrypted_password, "utf-8")
            ):
                user = User()
                # Dados de usuário
                user.first_name = user_bonde.first_name
                user.last_name = user_bonde.last_name
                user.username = user_bonde.email
                user.email = user_bonde.email
                user.set_password(password)
                # Permissões
                user.is_staff = True
                user.is_superuser = user_bonde.is_admin
                user.save()

                if not user.is_superuser:
                    user.groups.add(Group.objects.get(name="Mobilizador"))
                    user.save()

        return user


class BondeSiteBackend(BondeBackend):
    def authenticate(self, request, username, password, **kwargs):
        user = super(BondeSiteBackend, self).authenticate(
            request, username, password, **kwargs
        )

        if user and not user.is_superuser:
            host, port = request.get_host().split(":")

            user_bonde = UserBonde.objects.get(email=username)
            if port:
                host = host.replace(".localhost", ".org.br")

            if not user_bonde.communityuser_set.filter(
                community__dnshostedzone__domain_name=host
            ).exists():
                return

        return user
