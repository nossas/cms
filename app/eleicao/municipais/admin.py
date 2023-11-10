from django.contrib import admin

from .models import Candidatura, Vereador, Prefeito


admin.site.register(Candidatura)
admin.site.register(Vereador)
admin.site.register(Prefeito)
