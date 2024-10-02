"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from .views import OAuthLoginView, OAuthChangePasswordView, OAuthLogoutView, OAuthPasswordResetView, OAuthPasswordResetDoneView


urlpatterns = [
    path("sair/", OAuthLogoutView.as_view(), name="logout"),
    path("login/", OAuthLoginView.as_view(), name="login"),
    path("esqueci-minha-senha/", OAuthPasswordResetView.as_view(), name="reset-password"),
    path("esqueci-minha-senha/sucesso/", OAuthPasswordResetDoneView.as_view(), name="reset-password-done"),
    path("criar-nova-senha/<uidb64>/<token>/", OAuthChangePasswordView.as_view(), name="change-password"),
]
