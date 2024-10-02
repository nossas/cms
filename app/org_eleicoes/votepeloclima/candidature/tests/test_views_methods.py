import pytest

from collections import OrderedDict
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.test import override_settings
from django.urls import path, include

from org_eleicoes.votepeloclima.candidature.views.base import CandidatureBaseView
from org_eleicoes.votepeloclima.candidature.views.create import CreateUpdateCandidatureView


@pytest.fixture
def setup_oauth_urls():
    """Setup oauth apphook urls"""
    from org_eleicoes.votepeloclima.urls import urlpatterns

    urlpatterns = [
        path("oauth/", include(("contrib.oauth.urls", "oauth"))),
    ] + urlpatterns

    with override_settings(
        ROOT_URLCONF=type('DynamicUrlConf', (object,), {'urlpatterns': urlpatterns}),
        DEBUG=True
    ):
        yield


def test_base_view_form_list():
    from org_eleicoes.votepeloclima.candidature.forms import register_form_list

    assert CandidatureBaseView.form_list == register_form_list


def test_base_view_file_storage():
    from django.core.files.storage import default_storage

    assert CandidatureBaseView.file_storage == default_storage


def test_inherit_add_and_edit_base_view():
    assert issubclass(CreateUpdateCandidatureView, CandidatureBaseView)


def test_get_current_user_when_init_view():
    view = CandidatureBaseView()
    with pytest.raises(NotImplementedError):
        view.get_current_user()


@pytest.mark.django_db
def test_get_current_user_create(mocker):
    view = CreateUpdateCandidatureView()
    view.request = type("WSGIRequest", (object,), {"is_secure": lambda: False, "user": None})

    spy_cleaned_data = mocker.spy(view, "get_cleaned_data_for_step")

    user = view.get_current_user()
    spy_cleaned_data.assert_called_once_with("informacoes-pessoais")

    assert user is None


@pytest.mark.django_db
def test_get_current_user_create_with_email(mocker):
    from django.contrib.auth.models import User

    view = CreateUpdateCandidatureView()
    view.request = type("WSGIRequest", (object,), {"is_secure": lambda: False, "user": None})

    email = "test@localhost"
    user = User.objects.create(username=email, email=email)

    with mocker.patch.object(
        view,
        "get_cleaned_data_for_step",
        return_value={"properties": {"email": user.email}},
    ):
        assert view.get_current_user() == user


@pytest.mark.django_db
def test_get_instance_without_info():
    view = CandidatureBaseView()
    view.request = type("WSGIRequest", (object,), {"user": AnonymousUser()})
    view.storage = type("SessionStorage", (object,), {"data": {}})

    assert view.instance is None


@pytest.mark.django_db
def test_get_instance_with_email():
    from django.contrib.auth.models import User
    from org_eleicoes.votepeloclima.candidature.models import CandidatureFlow

    view = CandidatureBaseView()
    email = "test@localhost"
    user = User.objects.create(username=email, email=email)
    flow = CandidatureFlow.objects.create(user=user)
    data = {
        "step_data": {"informacoes-pessoais": {"informacoes-pessoais-email": [email]}}
    }

    view.request = type("WSGIRequest", (object,), {"user": AnonymousUser()})
    view.storage = type("SessionStorage", (object,), {"data": data})

    assert view.instance == flow


@pytest.mark.django_db
def test_get_instance_with_email():
    from django.contrib.auth.models import User
    from org_eleicoes.votepeloclima.candidature.models import CandidatureFlow

    view = CandidatureBaseView()
    email = "test@localhost"
    data = {
        "step_data": {"informacoes-pessoais": {"informacoes-pessoais-email": [email]}}
    }

    view.request = type("WSGIRequest", (object,), {"user": AnonymousUser()})
    view.storage = type("SessionStorage", (object,), {"data": data})

    assert view.instance is None


@pytest.mark.django_db
def test_get_instance_with_request_user():
    from django.contrib.auth.models import User
    from org_eleicoes.votepeloclima.candidature.models import CandidatureFlow

    view = CandidatureBaseView()
    email = "test@localhost"
    user = User.objects.create(username=email, email=email)
    flow = CandidatureFlow.objects.create(user=user)

    view.request = type("WSGIRequest", (object,), {"user": user})

    assert view.instance == flow


@pytest.mark.django_db
def test_remove_process_step_files():
    view = CandidatureBaseView()

    assert view.process_step_files("") is None


@pytest.mark.django_db
def test_create_user_when_process_step_infos(mocker, setup_oauth_urls):
    import datetime
    from django.contrib.auth.models import User
    from org_eleicoes.votepeloclima.candidature.forms import PersonalForm

    initial_data = {
        "legal_name": "Test Surname",
        "ballot_name": "Test",
        "birth_date": datetime.date(1992, 10, 12),
        "email": "test@localhost",
        "cpf": "123.456.789-01"
    }
    form = PersonalForm(data=initial_data)

    view = CandidatureBaseView()
    view.request = type("WSGIRequest", (object,), {
        "user": AnonymousUser,
        "is_secure": lambda: False
    })

    cleaned_data = {
        "view_name-current_step": "informacoes-pessoais",
        "informacoes-pessoais-email": "test@localhost",
        "informacoes-pessoais-legal_name": "Test Surname"
    }

    #
    with mocker.patch.object(
        view, "get_current_user", return_value=None
    ) and mocker.patch.object(
        view, "get_prefix", return_value="view_name"
    ) and mocker.patch.object(
        view, "get_form_step_data", return_value=cleaned_data
    ) and mocker.patch.object(
        view, "get_cleaned_data_for_step", return_value={}
    ) and mocker.patch.object(
        view, "get_form_list", return_value=OrderedDict(view.form_list)
    ):
        # Fake form response in get_form_step_data
        view.process_step(form=form)

        user = User.objects.get(email="test@localhost")

        assert user.username == "test@localhost"
        assert user.first_name == "Test"
        assert user.last_name == "Surname"
        assert user.is_active == False


@pytest.mark.django_db
def test_create_user_and_sendmail_when_is_new(mocker, setup_oauth_urls):
    mocker.patch("org_eleicoes.votepeloclima.candidature.views.base.send_confirmation_email")

    import datetime
    from django.contrib.auth.models import User
    from org_eleicoes.votepeloclima.candidature.forms import PersonalForm
    from org_eleicoes.votepeloclima.candidature.views.base import CandidatureBaseView, send_confirmation_email


    initial_data = {
        "legal_name": "Test Surname",
        "ballot_name": "Test",
        "birth_date": datetime.date(1992, 10, 12),
        "email": "test@localhost",
        "cpf": "123.456.789-01"
    }
    form = PersonalForm(data=initial_data)

    view = CandidatureBaseView()
    view.request = type("WSGIRequest", (object,), {
        "is_secure": lambda: False
    })

    cleaned_data = {
        "view_name-current_step": "informacoes-pessoais",
        "informacoes-pessoais-email": "test@localhost",
        "informacoes-pessoais-legal_name": "Test Surname"
    }

    with mocker.patch.object(
        view, "get_current_user", return_value=None
    ) and mocker.patch.object(
        view, "get_prefix", return_value="view_name"
    ) and mocker.patch.object(
        view, "get_form_step_data", return_value=cleaned_data
    ) and mocker.patch.object(
        view, "get_cleaned_data_for_step", return_value={}
    ) and mocker.patch.object(
        view, "get_form_list", return_value=OrderedDict(view.form_list)
    ):
        # Fake form response in get_form_step_data
        view.process_step(form=form)

        send_confirmation_email.assert_called_once_with(
            user=User.objects.get(email="test@localhost"),
            request=view.request
        )


@pytest.mark.django_db
def test_upsert_instance_create_flow_personal_step(mocker):
    import datetime
    from django.contrib.auth.models import User
    from org_eleicoes.votepeloclima.candidature.forms import PersonalForm

    user = User.objects.create(**{"username": "test@localhost", "email": "test@localhost"})
    current_step = "informacoes-pessoais"
    
    appoitments = {"appointment_1": True,"appointment_2": True}
    initial_data = {
        "legal_name": "Test Surname",
        "ballot_name": "Test",
        "birth_date": datetime.date(1992, 10, 12),
        "email": "test@localhost",
        "cpf": "123.456.789-01"
    }
    form = PersonalForm(data=initial_data)

    view = CandidatureBaseView()
    view.request = type("WSGIRequest", (object,), {"is_secure": lambda: False, "user": None})
    with mocker.patch.object(
        view, "get_cleaned_data_for_step", return_value=appoitments
    ):

        instance, created = view.upsert_instance(form, current_step, user)

        assert created == True
        assert instance.properties == {
            **appoitments,
            **initial_data
        }


@pytest.mark.django_db
def test_upsert_instance_update_flow_personal_step(mocker):
    import datetime
    from django.contrib.auth.models import User
    from org_eleicoes.votepeloclima.candidature.models import CandidatureFlow
    from org_eleicoes.votepeloclima.candidature.forms import PersonalForm

    user = User.objects.create(**{"username": "test@localhost", "email": "test@localhost"})
    flow = CandidatureFlow.objects.create(user=user)
    current_step = "informacoes-pessoais"
    
    appoitments = {"appointment_1": True,"appointment_2": True}
    initial_data = {
        "legal_name": "Test Surname",
        "ballot_name": "Test",
        "birth_date": datetime.date(1992, 10, 12),
        "email": "test@localhost",
        "cpf": "123.456.789-01"
    }
    form = PersonalForm(data=initial_data)

    view = CandidatureBaseView()
    view.request = type("WSGIRequest", (object,), {"is_secure": lambda: False, "user": None})
    with mocker.patch.object(
        view, "get_cleaned_data_for_step", return_value=appoitments
    ):

        instance, created = view.upsert_instance(form, current_step, user)

        assert created == False
        assert instance.id == flow.id
        assert instance.properties == initial_data


@pytest.mark.django_db
def test_call_upsert_instance_when_user(mocker):
    from django.contrib.auth.models import User
    from org_eleicoes.votepeloclima.candidature.forms import ApplicationForm
    from org_eleicoes.votepeloclima.candidature.models import CandidatureFlow

    user = User.objects.create(username="test@localhost", email="test@localhost")
    CandidatureFlow.objects.create(user=user)

    view = CandidatureBaseView()
    view.request = type("WSGIRequest", (object,), {
        "is_secure": lambda: False
    })

    form_data = {
        "candidature_base_view-current_step": "informacoes-de-candidatura"
    }
    initial_data = {
        "number_id": 13,
        "intended_position": "prefeitura",
        "state": "11",
        "city": "1101",
        "political_party": "pt"
    }
    form = ApplicationForm(data=initial_data)

    upsert_instance_spy = mocker.spy(view, "upsert_instance")

    with mocker.patch.object(
        view, "get_current_user", return_value=user
    ) and mocker.patch.object(
        view, "get_form_step_data", return_value=form_data
    ) and mocker.patch.object(
        view, "get_form_list", return_value=OrderedDict(view.form_list)
    ):
        view.process_step(form)

        upsert_instance_spy.assert_called_once_with(
            form, "informacoes-de-candidatura", user
        )


@pytest.mark.django_db
def test_form_instance_none():
    view = CandidatureBaseView()
    view.request = type("WSGIRequest", (object,), {
        "is_secure": lambda: False,
        "user": None,
    })

    assert view.get_form_instance("step") is None


@pytest.mark.django_db
def test_form_instance_by_user():
    from django.contrib.auth.models import User
    from org_eleicoes.votepeloclima.candidature.models import CandidatureFlow

    user = User.objects.create(username="test@localhost", email="test@localhost")
    instance = CandidatureFlow.objects.create(user=user)

    view = CandidatureBaseView()
    view.request = type("WSGIRequest", (object,), {
        "is_secure": lambda: False,
        "user": user,
    })

    assert view.get_form_instance("step") == instance


@pytest.mark.django_db
def test_form_instance_by_storage():
    from django.contrib.auth.models import User
    from org_eleicoes.votepeloclima.candidature.models import CandidatureFlow

    user = User.objects.create(username="test@localhost", email="test@localhost")
    instance = CandidatureFlow.objects.create(user=user)

    view = CandidatureBaseView()
    view.request = type("WSGIRequest", (object,), {
        "is_secure": lambda: False,
        "user": AnonymousUser(),
    })
    view.storage = type("SessionStorage", (object,), {"data": {
        "step_data": {
            "informacoes-pessoais": {
                "informacoes-pessoais-email": ["test@localhost"]
            }
        }
    }})

    assert view.get_form_instance("informacoes-pessoais") == instance