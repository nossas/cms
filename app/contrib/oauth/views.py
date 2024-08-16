from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.views import (
    LoginView,
    PasswordResetConfirmView,
    INTERNAL_RESET_SESSION_TOKEN,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView
)
from django.contrib.auth import login as auth_login
from django.urls import reverse, reverse_lazy

from .forms import OAuthPasswordResetForm


class OAuthLoginView(LoginView):
    template_name = "oauth/login.html"

    def get_success_url(self):
        if hasattr(settings, 'OAUTH_REDIRECT_LOGIN_URL'):
            return settings.OAUTH_REDIRECT_LOGIN_URL
        return self.get_redirect_url() or reverse("oauth:index")


class OAuthChangePasswordView(PasswordResetConfirmView):
    template_name = "oauth/change_password.html"
    post_reset_login = True
    post_reset_login_backend = "contrib.oauth.backends.OAuthBackend"

    def form_valid(self, form):
        user = form.save(commit=False)
        # Active user after reset password
        user.is_active = True
        user.save()

        try:
            del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        except KeyError as err:
            print(err)

        if self.post_reset_login:
            auth_login(self.request, user, self.post_reset_login_backend)
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        if hasattr(settings, 'OAUTH_REDIRECT_LOGIN_URL'):
            return settings.OAUTH_REDIRECT_LOGIN_URL
        return reverse("oauth:index")


class OAuthLogoutView(LogoutView):

    def get_success_url(self):
        return reverse("oauth:login")


class OAuthPasswordResetView(PasswordResetView):
    template_name = "oauth/password_reset_form.html"
    success_url = reverse_lazy("oauth:reset-password-done")
    form_class = OAuthPasswordResetForm
    subject_template_name = "oauth/email/password_reset_subject.txt"
    email_template_name = "oauth/email/password_reset_confirm.html"


class OAuthPasswordResetDoneView(PasswordResetDoneView):
    template_name = "oauth/password_reset_done.html"