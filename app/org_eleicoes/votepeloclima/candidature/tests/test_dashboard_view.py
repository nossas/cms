import pytest

from django.test import override_settings
from django.urls import path, reverse

from model_bakery import baker


@pytest.fixture(autouse=True)
def setup_urls():
    from django.contrib.sites.models import Site
    from contrib.ds.models import Theme
    from org_eleicoes.votepeloclima.urls import urlpatterns, include

    site = Site.objects.get(id=1)
    site.domain = "testserver"
    site.save()

    Theme.objects.create(site=site, scss_json={"colors": {}})

    urlpatterns = [
        path("oauth/", include(("contrib.oauth.urls", "oauth"))),
    ] + urlpatterns

    with override_settings(
        ROOT_URLCONF=type('DynamicUrlConf', (object,), {'urlpatterns': urlpatterns}),
        DEBUG=True
    ):
        yield


@pytest.mark.django_db
def test_redirect_dashboard_when_not_logged(client):
    response = client.get(reverse("dashboard"))

    assert response.status_code == 302
    assert response.url.startswith(reverse("oauth:login") + "?next=")


@pytest.mark.django_db
def test_get_dashboard_when_logged(client):
    from django.contrib.auth.models import User
    from org_eleicoes.votepeloclima.candidature.choices import CandidatureFlowStatus
    from org_eleicoes.votepeloclima.candidature.models import CandidatureFlow, Candidature

    user = User.objects.create_user(username="test@localhost", password="test123")
    candidature = baker.make(Candidature, flags=[], appointments=[])
    flow = baker.make(CandidatureFlow, candidature=candidature, user=user, status=CandidatureFlowStatus.submitted)

    assert flow.status == CandidatureFlowStatus.submitted

    client.login(username="test@localhost", password="test123")
    response = client.post(reverse("dashboard"), data={"request_change": True})

    assert response.status_code == 302
    assert CandidatureFlow.objects.first().status == CandidatureFlowStatus.editing



