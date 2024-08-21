import hashlib

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.models import User, AnonymousUser
from django.db.models import Q
from django.views.generic import TemplateView, ListView

from django.http import HttpResponseForbidden
from django.urls import reverse_lazy, reverse
from django.core.files.storage import default_storage

from formtools.wizard.views import NamedUrlSessionWizardView

from contrib.oauth.utils import send_confirmation_email
from ..models import CandidatureFlow, CandidatureFlowStatus, Candidature
from ..forms import CandidatureSearchSideForm, CandidatureSearchTopForm, register_form_list, ProposeForm, AppointmentForm
from ..locations_utils import get_ufs, get_choices
from ..choices import (
    PoliticalParty,
    IntendedPosition,
    Color,
    Gender,
    Sexuality,
)

initial_step_name = register_form_list[2][0]
disable_edit_steps = [
    "informacoes-pessoais",
    "informacoes-de-candidatura",
    "captcha",
    "compromissos",
]


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
        if not self._instance and isinstance(self.request.user, AnonymousUser):
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
        elif isinstance(self.request.user, User):
            self._instance = self.request.user.candidatureflow

        return self._instance

    instance = property(_get_instance)

    def post(self, *args, **kwargs):
        request = self.request
        if "wizard_goto_last" in request.POST:
            form = self.get_form(data=request.POST, files=request.FILES)

            if form.is_valid():
                self.storage.set_step_data(self.steps.current, self.process_step(form))
                self.storage.set_step_files(
                    self.steps.current, self.process_step_files(form)
                )
                # Move to last step
                self.storage.current_step = self.steps.all[-1]
                if self.request.user.is_active:
                    return redirect("/area-restrita")
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

            send_confirmation_email(user=user, request=self.request)

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
        print("asdadasdasdasd")
        form_data = super().process_step(form)
        current_step = form_data[f"{self.get_prefix(self.request)}-current_step"]
        user = self.get_current_user()

        print(form_data)
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
            print("asdadasdasdasd")
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

        context.update(
            {
                "next_step_title": self.get_next_step_title(),
                "editing": self.storage.extra_data.get("editing", False),
            }
        )
        return context

    def done(self, form_list, form_dict, **kwargs):
        user = self.get_current_user()
        flow = CandidatureFlow.objects.get(user=user)
        values = {}

        for step, form in form_dict.items():
            if step not in ("captcha", "checkout"):
                if isinstance(form, ProposeForm):
                    values.update({"proposes": form.cleaned_data.get("properties")})
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
        is_draft = (
            self.request.user.candidatureflow
            and self.request.user.candidatureflow.status == CandidatureFlowStatus.draft
        )

        is_steps = bool(
            len(
                list(
                    filter(
                        lambda x: self.request.path.endswith(f"{x}/"),
                        disable_edit_steps,
                    )
                )
            )
        )

        return is_draft and not is_steps

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return HttpResponseForbidden(
                "You do not have permission to edit Candidature"
            )
        return super().dispatch(request, *args, **kwargs)

    def get_current_user(self):
        return self.request.user

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)
        context["editing"] = True
        return context


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "candidature/dashboard.html"
    login_url = reverse_lazy("oauth:login")
    steps_hide_on_checkout = ("captcha", "checkout", "compromissos")

    def get_checkout_steps(self):
        checkout_steps = []

        for step_name, form_class in register_form_list:
            if step_name not in self.steps_hide_on_checkout:
                obj = CandidatureFlow.objects.get(user=self.request.user)
                form = form_class(instance=obj, data=obj.properties, disabled=True)
                step_dict = dict(
                    name=step_name,
                    form=form,
                    is_valid=form.is_valid(),
                )
                if step_name not in disable_edit_steps:
                    step_dict["edit_url"] = reverse(
                        "register_edit_step", kwargs={"step": step_name}
                    )

                checkout_steps.append(step_dict)

        return checkout_steps

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.request.user.is_staff:
            checkout_steps = self.get_checkout_steps()
            # checkout_steps = []
            context.update(
                {
                    "flow": self.request.user.candidatureflow,
                    "checkout_steps": checkout_steps,
                }
            )

        return context


class AddressView(View):
    def get(self, request, *args, **kwargs):
        state = request.GET.get("state")
        cities = get_choices(state)
        return JsonResponse([{'code': code, 'name': name} for code, name in cities], safe=False)


class ProposesMixin:
    def get_proposes(self, candidature):
        proposes_list = []

        for field_name, value in candidature.proposes.items():
            if value:
                proposes_list.append({
                    "label": ProposeForm().fields[field_name].checkbox_label,
                    "description": value
                })

        return proposes_list


class CandidatureSearchView(ListView, ProposesMixin):
    model = Candidature
    template_name = "candidature/candidature_search.html"
    context_object_name = "candidatures"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(candidatureflow__status__in=[CandidatureFlowStatus.is_valid, CandidatureFlowStatus.editing])

        form_top = CandidatureSearchTopForm(self.request.GET or None)
        form_side = CandidatureSearchSideForm(self.request.GET or None)

        if form_top.is_valid() and form_side.is_valid():
            cleaned_data = {**form_top.cleaned_data, **form_side.cleaned_data}

            for field in ['state', 'city', 'intended_position', 'political_party', 'gender', 'color', 'sexuality', 'ballot_name']:
                values = cleaned_data.get(field)
                if values:
                    if isinstance(values, list):
                        queryset = queryset.filter(**{f"{field}__in": values})
                    else:
                        queryset = queryset.filter(**{field: values})
            
            keyword = self.request.GET.get('keyword')
            if keyword:
                queryset = queryset.filter(
                    Q(short_description__icontains=keyword) |
                    Q(milestones__icontains=keyword) |
                    Q(proposes__icontains=keyword) |
                    Q(appointments__icontains=keyword)
                )
            
            is_collective_mandate = self.request.GET.get('is_collective_mandate')
            if is_collective_mandate:
                queryset = queryset.filter(is_collective_mandate=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form_top = CandidatureSearchTopForm(self.request.GET or None)
        form_side = CandidatureSearchSideForm(self.request.GET or None)

        # Atualizar as cidades com base no estado selecionado
        state = self.request.GET.get('state')
        if state:
            form_top.update_city_choices(state)

        context['form_top'] = form_top
        context['form_side'] = form_side
        
        candidature = self.get_queryset().first()
        if candidature:
            context['proposes'] = self.get_proposes(candidature)

        return context


class PublicCandidatureView(View, ProposesMixin):
    template_name = "candidature/candidate_profile.html"

    def get(self, request, slug):
        candidature = get_object_or_404(Candidature, slug=slug)
        context = {
            "candidature": candidature,
            "proposes": self.get_proposes(candidature),
        }

        # Verifica se a candidatura está aprovada
        if candidature.status() != CandidatureFlowStatus.is_valid.label:
            return render(request, 'candidature/not_approved.html', context)

        return render(request, self.template_name, context)
