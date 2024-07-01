from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
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