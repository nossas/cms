from django.urls import path

from .views import (
    get_all_traefik_config,
    create_initial_config,
    create_cms_config,
    create_public_config,
    create_whoami_config,
    delete_public_config
)

urlpatterns = [
    path("config/", get_all_traefik_config, name="config"),
    path("create-config/", create_initial_config, name="create-config"),
    path("create-cms-config/", create_cms_config, name="create-cms-config"),
    path("create-public-config/", create_public_config, name="create-public-config"),
    path("delete-public-config/", delete_public_config, name="delete-public-config"),
    path("create-whoami-config/", create_whoami_config, name="create-whoami-config"),
]
