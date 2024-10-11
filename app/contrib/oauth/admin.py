from django.contrib import admin

from .models import Token


class TokenAdmin(admin.ModelAdmin):
    list_display = ("user", "key")
    fields = ("user", )


admin.site.register(Token, TokenAdmin)