from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetConfirmView, INTERNAL_RESET_SESSION_TOKEN
from django.contrib.auth import login as auth_login
from django.urls import reverse_lazy, reverse


class OAuthIndexView(LoginRequiredMixin, TemplateView):
    template_name = "oauth/index.html"
    login_url = reverse_lazy("oauth:login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class OAuthLoginView(LoginView):
    template_name = "oauth/login.html"

    def get_success_url(self):
        return reverse("oauth:index")


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
        return reverse("oauth:index")
    # form_class = PasswordChangeForm

    # def form_valid(self, form):
    #     return super().form_valid()