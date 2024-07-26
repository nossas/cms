from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy, reverse
from django.core.files.storage import default_storage

from formtools.wizard.views import NamedUrlSessionWizardView

from contrib.oauth.utils import send_confirmation_email
from .models import CandidatureFlow, CandidatureFlowStatus, Candidature
from .forms import register_form_list, InitialForm, FlagForm, AppointmentForm, ProfileForm
from .locations_utils import get_choices


initial_step_name = register_form_list[2][0]


class BaseRegisterView(NamedUrlSessionWizardView):
    form_list = register_form_list
    template_name = "candidature/wizard_form.html"
    file_storage = default_storage
    # user = None

    # def dispatch(self, request, *args, **kwargs):
    #     response = super().dispatch(request, *args, **kwargs)
        
    #     # Atualiza o atributo instance do storage com o Fluxo de Candidatura relacionado ao usuário preenchido no e-mail
    #     # Candidatura deve estar habilita como draft
    #     data = self.storage.data.get("step_data")
    #     if "informacoes-iniciais" in data and "informacoes-iniciais-email" in data.get("informacoes-iniciais"):
    #         email = self.storage.data.get("step_data").get("informacoes-iniciais").get("informacoes-iniciais-email")[0]
    #         user = User.objects.get(email=email)
    #         self.storage.instance, created = CandidatureFlow.objects.get_or_create(CandidatureFlow.objects.get_or_create(user=user))

    #     return response

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

        return created

    def process_step(self, form):
        form_data = super().process_step(form)
        # import ipdb;ipdb.set_trace()
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

        # import ipdb;ipdb.set_trace()
        return form_data


class RegisterView(BaseRegisterView):
    steps_hide_on_checkout = ["captcha"]

    def render_done(self, form, **kwargs):
        revalid = True
        return super().render_done(form, **kwargs)

    def get_template_names(self):
        if self.steps.current == "checkout":
            return "candidature/checkout.html"
        elif self.steps.current == "bandeiras-da-sua-candidatura":
            return "candidature/bandeiras_da_sua_candidatura.html"
        return super().get_template_names()

    def get_next_step_title(self):
        if self.steps.next:
            next_step = self.steps.next
            form_class = self.get_form_list().get(next_step)
            if form_class:
                return form_class().Meta.title
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
                    # data = self.get_cleaned_data_for_step(step)
                    checkout_steps.append(
                        dict(
                            name=step,
                            edit_url=reverse(self.url_name, kwargs={"step": step}),
                            form=form_class(disabled=True, instance=instance),
                            # data=data,
                        )
                    )

            context.update({"checkout_steps": checkout_steps})

        context.update({"next_step_title": self.get_next_step_title()})
        return context

    def done(self, form_list, form_dict, **kwargs):
        user = self.get_current_user()
        flow = CandidatureFlow.objects.get(user=user)
        values = {}

        for step, form in form_dict.items():
            if step not in self.steps_hide_on_checkout and step != "checkout":
                if isinstance(form, FlagForm):
                    values.update({"flags": form.cleaned_data})
                elif isinstance(form, AppointmentForm):
                    values.update({"appointments": form.cleaned_data})
                else:
                    values.update(form.cleaned_data)

        obj = Candidature.objects.create(**values)
        flow.candidature = obj
        flow.status = CandidatureFlowStatus.submitted
        flow.save()

        print("Enviar e-mail de cadastro enviado")

        return redirect("/")


class EditRegisterView(LoginRequiredMixin, RegisterView):
    login_url = reverse_lazy("oauth:login")

    def has_permission(self):
        return self.request.user.candidatureflow and self.request.user.candidatureflow.status == CandidatureFlowStatus.draft
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return HttpResponseForbidden("You do not have permission to edit Candidature")
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
                    copyKey = key.replace(f'{step}-', '')
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
                for key in list(filter(lambda x: x.startswith(step_name), candidature_flow.properties.keys())):
                    initial_data[key.replace(step_name + "-", "")] = candidature_flow.properties.get(key)[0]
                
                checkout_steps.append(dict(
                    name=step_name,
                    edit_url=reverse("register_edit_step", kwargs={"step": step_name}),
                    form=form_class(data=initial_data, disabled=True)
                ))
        
        return checkout_steps


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.request.user.is_staff:
            checkout_steps = self.get_checkout_steps()
            # checkout_steps = []
            context.update({
                "candidature_flow": self.request.user.candidatureflow,
                "checkout_steps": checkout_steps
            })

        return context


class AddressView(View):
    def get(self, request, *args, **kwargs):
        state = request.GET.get('state')
        cities = get_choices(state)
        return JsonResponse([{'code': code, 'name': name} for code, name in cities], safe=False)
