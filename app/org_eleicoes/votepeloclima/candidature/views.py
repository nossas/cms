import hashlib

from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic import TemplateView, ListView
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy, reverse
from django.core.files.storage import default_storage

from formtools.wizard.views import NamedUrlSessionWizardView

from contrib.oauth.utils import send_confirmation_email
from .models import CandidatureFlow, CandidatureFlowStatus, Candidature
from .forms import register_form_list, ProposeForm, AppointmentForm
from .locations_utils import get_ufs, get_choices
from .choices import (
    PoliticalParty,
    IntendedPosition,
    Color,
    Gender,
    Sexuality,
)


initial_step_name = register_form_list[2][0]


def files_is_equal(file1, file2):
    hash1_sha256 = hashlib.sha256()
    for block in iter(lambda: file1.read(4096), b""):
        hash1_sha256.update(block)

    hash2_sha256 = hashlib.sha256()
    for block in iter(lambda: file2.read(4096), b""):
        hash2_sha256.update(block)

    return hash1_sha256.hexdigest() == hash2_sha256.hexdigest()


class BaseRegisterView(NamedUrlSessionWizardView):
    _instance = None
    form_list = register_form_list
    template_name = "candidature/wizard_form.html"
    file_storage = default_storage

    def _get_instance(self):
        if not self._instance:
            step_name = "informacoes-pessoais"
            email = (
                self.storage.data.get("step_data", {})
                .get(step_name, {})
                .get(f"{step_name}-email", [None])[0]
            )
            try:
                user = User.objects.get(email=email)
                self._instance = user.candidatureflow
            except User.DoesNotExist:
                pass

        return self._instance

    instance = property(_get_instance)

    def post(self, *args, **kwargs):
        request = self.request
        if "wizard_goto_last" in request.POST:
            form = self.get_form(data=request.POST, files=request.FILES)
            
            if form.is_valid():
                self.storage.set_step_data(self.steps.current, self.process_step(form))
                self.storage.set_step_files(self.steps.current, self.process_step_files(form))
                # Move to last step
                self.storage.current_step = self.steps.all[-1]
                return self.render(self.get_form())

        return super().post(*args, **kwargs)

    def get_current_user(self):
        data = self.get_cleaned_data_for_step(initial_step_name)
        if data:
            return User.objects.get(email=data["properties"]["email"])

        return None

    def create_user(self, **values):
        user, created = User.objects.get_or_create(**values)

        if created:
            user.is_active = False
            user.save()

            send_confirmation_email(
                user,
                self.request,
                email_template_name="candidature/activation_email.html",
            )

        return user

    def save_obj(self, instance, form):
        if form.is_valid():
            for field, value in form.cleaned_data.items():
                if field == "properties":
                    instance.properties.update(value)
                elif field not in ("photo", "video"):
                    setattr(instance, field, value)
                else:
                    instance_field = getattr(instance, field)
                    if not instance_field:
                        setattr(instance, field, value)
                    elif not files_is_equal(instance_field.file, value.file):
                        # Remove old files
                        instance_field.delete()
                        setattr(instance, field, value)

            instance.save()

        return instance

    def upsert_instance(self, form, current_step, user):
        instance, created = CandidatureFlow.objects.get_or_create(user=user)

        if created:
            for step, FormClass in register_form_list[1:]:
                if step == current_step:
                    break

                data = self.get_cleaned_data_for_step(step)
                if "properties" in data:
                    data.update(data.get("properties"))

                instance = self.save_obj(instance, form=FormClass(data=data))

        self.save_obj(instance, form)

        return instance, created

    def process_step_files(self, form):
        # Save file method on save_obj in model
        return None

    def process_step(self, form):
        form_data = super().process_step(form)
        current_step = form_data[f"{self.get_prefix(self.request)}-current_step"]
        user = self.get_current_user()

        if current_step == initial_step_name and not user:
            email = form_data[current_step + "-email"]
            name = form_data[current_step + "-legal_name"]

            values = {
                "username": email,
                "email": email,
                "first_name": name.split(" ")[0],
                "last_name": " ".join(name.split(" ")[:-1]),
            }
            user = self.create_user(**values)

        if user:
            self.upsert_instance(form, current_step, user)

        if current_step == "complemente-seu-perfil":
            self.storage.extra_data["editing"] = True

        return form_data

    def get_form_instance(self, step):
        return self.instance


class RegisterView(BaseRegisterView):
    steps_hide_on_checkout = ["captcha", "compromissos"]

    def render_done(self, form, **kwargs):
        revalid = True
        return super().render_done(form, **kwargs)

    def get_template_names(self):
        if self.steps.current == "checkout":
            return "candidature/checkout.html"
        elif self.steps.current == "suas-propostas":
            return "candidature/suas_propostas.html"
        elif self.steps.current == "captcha":
            return "candidature/captcha.html"
        elif self.steps.current == "informacoes-pessoais":
            return "candidature/informacoes_pessoais.html"
        elif self.steps.current == "compromissos":
            return "candidature/compromissos.html"
        return super().get_template_names()

    def get_next_step_title(self):
        if self.steps.next:
            next_step = self.steps.next
            form_class = self.get_form_list().get(next_step)
            if hasattr(form_class.Meta, "title"):
                return form_class.Meta.title
        return ""

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)
        checkout_steps = []
        if self.steps.current == "checkout":
            user = self.get_current_user()
            instance = CandidatureFlow.objects.get(user=user)
            # import ipdb;ipdb.set_trace()
            for step, form_class in self.get_form_list().items():
                if step not in self.steps_hide_on_checkout:
                    form = form_class(disabled=True, instance=instance)
                    checkout_steps.append(
                        dict(
                            name=step,
                            title=form_class.Meta.title,
                            edit_url=reverse(self.url_name, kwargs={"step": step}),
                            form=form,
                        )
                    )

            context.update({"checkout_steps": checkout_steps})

        if hasattr(form.Meta, "title"):
            context.update({"step_title": form.Meta.title})
        if hasattr(form.Meta, "description"):
            context.update({"step_description": form.Meta.description})

        context.update({
            "next_step_title": self.get_next_step_title(),
            "editing": self.storage.extra_data.get("editing", False)
        })
        return context

    def done(self, form_list, form_dict, **kwargs):
        user = self.get_current_user()
        flow = CandidatureFlow.objects.get(user=user)
        values = {}

        for step, form in form_dict.items():
            if step not in ("captcha", "checkout"):
                if isinstance(form, ProposeForm):
                    values.update({"flags": form.cleaned_data.get("properties")})
                elif isinstance(form, AppointmentForm):
                    values.update({"appointments": form.cleaned_data.get("properties")})
                else:
                    cleaned = form.cleaned_data.copy()
                    properties = cleaned.pop("properties", {})
                    values.update({**properties, **cleaned})

        obj = Candidature.objects.create(**values)
        flow.candidature = obj
        flow.status = CandidatureFlowStatus.submitted
        flow.save()

        print("Enviar e-mail de cadastro enviado")

        return redirect("/")


class EditRegisterView(LoginRequiredMixin, RegisterView):
    login_url = reverse_lazy("oauth:login")

    def has_permission(self):
        return (
            self.request.user.candidatureflow
            and self.request.user.candidatureflow.status == CandidatureFlowStatus.draft
        )

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return HttpResponseForbidden(
                "You do not have permission to edit Candidature"
            )
        return super().dispatch(request, *args, **kwargs)

    def get_form_initial(self, step):
        """
        Returns a dictionary which will be passed to the form for `step`
        as `initial`. If no initial data was provided while initializing the
        form wizard, an empty dictionary will be returned.
        """
        initial_data = {}
        if step not in self.steps_hide_on_checkout:
            cflow = self.request.user.candidatureflow

            for key, value in cflow.properties.items():
                if key.startswith(step):
                    copyKey = key.replace(f"{step}-", "")
                    initial_data[copyKey] = value[0]

        return self.initial_dict.get(step, initial_data)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "candidature/dashboard.html"
    login_url = reverse_lazy("oauth:login")
    steps_hide_on_checkout = ("captcha", "checkout", "compromissos")

    def get_checkout_steps(self):
        checkout_steps = []
        candidature_flow = self.request.user.candidatureflow

        for step_name, form_class in register_form_list:
            if step_name not in self.steps_hide_on_checkout:
                initial_data = {}
                for key in list(
                    filter(
                        lambda x: x.startswith(step_name),
                        candidature_flow.properties.keys(),
                    )
                ):
                    initial_data[key.replace(step_name + "-", "")] = (
                        candidature_flow.properties.get(key)[0]
                    )

                checkout_steps.append(
                    dict(
                        name=step_name,
                        edit_url=reverse(
                            "register_edit_step", kwargs={"step": step_name}
                        ),
                        form=form_class(data=initial_data, disabled=True),
                    )
                )

        return checkout_steps

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.request.user.is_staff:
            checkout_steps = self.get_checkout_steps()
            # checkout_steps = []
            context.update(
                {
                    "candidature_flow": self.request.user.candidatureflow,
                    "checkout_steps": checkout_steps,
                }
            )

        return context


class AddressView(View):
    def get(self, request, *args, **kwargs):
        state = request.GET.get("state")
        cities = get_choices(state)
        return JsonResponse(
            [{"code": code, "name": name} for code, name in cities], safe=False
        )


class CandidatureSearchView(ListView):
    model = Candidature
    template_name = "candidature/candidature_search.html"
    context_object_name = "candidatures"

    def get_queryset(self):
        queryset = super().get_queryset()

        ballot_name = self.request.GET.get('ballot_name')
        if ballot_name:
            queryset = queryset.filter(ballot_name__icontains=ballot_name)

        intended_position = self.request.GET.get('intended_position')
        if intended_position:
            queryset = queryset.filter(intended_position__icontains=intended_position)

        political_party = self.request.GET.get('political_party')
        if political_party:
            queryset = queryset.filter(political_party__icontains=political_party)

        state = self.request.GET.get('state')
        if state:
            queryset = queryset.filter(state__icontains=state)

        city = self.request.GET.get('city')
        if city:
            queryset = queryset.filter(city__icontains=city)

        gender = self.request.GET.get('gender')
        if gender:
            queryset = queryset.filter(gender__icontains=gender)

        color = self.request.GET.get('color')
        if color:
            queryset = queryset.filter(color__icontains=color)
        
        sexuality = self.request.GET.get('sexuality')
        if sexuality:
            queryset = queryset.filter(sexuality__icontains=sexuality)
        
        keyword = self.request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(short_description__icontains=keyword) |
                Q(milestones__icontains=keyword) |
                Q(flags__icontains=keyword) |
                Q(appointments__icontains=keyword)
            )
        
        is_collective_mandate = self.request.GET.get('is_collective_mandate')
        if is_collective_mandate:
            queryset = queryset.filter(is_collective_mandate=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sexuality_choices'] = Sexuality.choices
        context['gender_choices'] = Gender.choices
        context['color_choices'] = Color.choices
        context['intended_position_choices'] = IntendedPosition.choices
        context['political_party_choices'] = PoliticalParty.choices
        context['states'] = get_ufs()
        selected_state = self.request.GET.get('state')
        if selected_state:
            context['cities'] = get_choices(selected_state)
        else:
            context['cities'] = []
        return context
