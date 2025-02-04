import pytest
from collections import OrderedDict

from formtools.wizard.views import StepsHelper, normalize_name

from org_eleicoes.votepeloclima.candidature.views.base import CandidatureBaseView
from org_eleicoes.votepeloclima.candidature.forms.register import (
    ProfileForm,
    AppointmentForm,
    CheckoutForm,
    register_form_list,
)


def test_add_form_title_context(mocker):
    view = CandidatureBaseView()
    view.request = type("WSGIRequest", (object,), {"is_secure": lambda: False, "user": None})
    view.prefix = normalize_name(view.__class__.__name__)
    view.steps = StepsHelper(view)
    view.storage = type(
        "SessionStorage",
        (object,),
        {"data": {}, "extra_data": {}, "current_step": "complemente-seu-perfil"},
    )

    form = ProfileForm()

    with mocker.patch.object(
        view, "get_form_list", return_value=OrderedDict(view.form_list)
    ):
        context = view.get_context_data(form)

        assert "step_title" in context
        assert context["step_title"] == form.Meta.title


def test_add_form_description_context(mocker):
    view = CandidatureBaseView()
    view.request = type("WSGIRequest", (object,), {"is_secure": lambda: False, "user": None})
    view.prefix = normalize_name(view.__class__.__name__)
    view.steps = StepsHelper(view)
    view.storage = type(
        "SessionStorage",
        (object,),
        {"data": {}, "extra_data": {}, "current_step": "compromissos"},
    )

    form = AppointmentForm()

    with mocker.patch.object(
        view, "get_form_list", return_value=OrderedDict(view.form_list)
    ):
        context = view.get_context_data(form)

        assert "step_description" in context
        assert context["step_description"] == form.Meta.description


@pytest.mark.django_db
def test_context_checkout_steps_with_forms_filleds_and_disabled(mocker):
    from django.contrib.auth.models import User
    from org_eleicoes.votepeloclima.candidature.models import CandidatureFlow

    user = User.objects.create(email="test@localhost", username="test@localhost")
    instance = CandidatureFlow.objects.create(user=user)

    view = CandidatureBaseView()
    view.request = type("WSGIRequest", (object,), {"is_secure": lambda: False, "user": None})
    view.prefix = normalize_name(view.__class__.__name__)
    view.steps = StepsHelper(view)
    view.storage = type(
        "SessionStorage",
        (object,),
        {"data": {}, "extra_data": {}, "current_step": "checkout"},
    )

    with mocker.patch.object(
        view, "get_current_user", return_value=user
    ) and mocker.patch.object(
        view, "get_form_list", return_value=OrderedDict(view.form_list)
    ):
        form = CheckoutForm()
        context = view.get_context_data(form)

        assert len(context["checkout_steps"]) == len(register_form_list) - 2

        for step in context["checkout_steps"]:
            assert step["form"].instance == instance
            assert step["form"].disabled == True


@pytest.mark.django_db
def test_flag_editing_when_process_step_next_is_checkout(mocker):
    from django.contrib.auth.models import User
    from org_eleicoes.votepeloclima.candidature.models import CandidatureFlow
    from org_eleicoes.votepeloclima.candidature.forms.register import ProfileForm

    user = User.objects.create(email="test@localhost", username="test@localhost")
    instance = CandidatureFlow.objects.create(user=user)

    view = CandidatureBaseView()

    extra_data = {}
    view.storage = type(
        "SessionStorage",
        (object,),
        {
            "data": {},
            "extra_data": extra_data,
            "current_step": "complemente-seu-perfil",
        },
    )
    view.request = type("WSGIRequest", (object,), {"is_secure": lambda: False})

    mocker.patch.object(view, "get_next_step", return_value="checkout")

    data = {
        "candidature_base_view-current_step": "complemente-seu-perfil"
    }

    form = ProfileForm(data=data)

    with mocker.patch.object(
        view, "get_current_user", return_value=user
    ):
        view.process_step(form)

        assert extra_data.get("editing") == True
