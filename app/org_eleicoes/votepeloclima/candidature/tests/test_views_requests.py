import pytest

from django.test import override_settings
from django.urls import path, re_path, reverse

from org_eleicoes.votepeloclima.candidature.views.base import CandidatureBaseView


@pytest.fixture(autouse=True)
def setup_view_urls():
    from django.contrib.sites.models import Site
    from org_eleicoes.votepeloclima.urls import urlpatterns

    Site.objects.filter(id=1).update(domain="testserver")

    view = CandidatureBaseView.as_view(
        url_name="step",
        done_step_name="done"
    )

    urlpatterns = [
        re_path(r"^step/(?P<step>.+)/$", view, name="step"),
        path('step/', view, name="step_index"),
    ] + urlpatterns

    with override_settings(
        ROOT_URLCONF=type('DynamicUrlConf', (object,), {'urlpatterns': urlpatterns}),
        DEBUG=True
    ):
        yield


@pytest.mark.django_db
def test_get_base_view_index_with_redirect(client):
    response = client.get(reverse("step_index"))

    assert response.status_code == 302