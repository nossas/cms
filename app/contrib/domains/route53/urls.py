from django.urls import path

from .views import index, detail, record

urlpatterns = [
    path("", index, name="index"),
    path("hostedzone/<str:hosted_zone_id>/", detail, name="detail"),
    path(
        "hostedzone/<str:hosted_zone_id>/<str:record_name>/<str:record_type>",
        record,
        name="record",
    ),
]
