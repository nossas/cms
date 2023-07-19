from django.apps import AppConfig


class AdminStyledConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_styled'
    default_site = 'admin_styled.admin.site'