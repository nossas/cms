from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy,reverse
from django.core.files.storage import DefaultStorage


from formtools.wizard.views import NamedUrlSessionWizardView

from contrib.oauth.utils import send_confirmation_email
from .models import CandidatureFlow, CandidatureFlowStatus, Candidature
from .forms import register_form_list, InitialForm, FlagForm, AppointmentForm, ProfileForm
from .locations_utils import get_choices


class RegisterView(NamedUrlSessionWizardView):
    form_list = register_form_list
    steps_hide_on_checkout = ["captcha"]
    template_name = "candidature/wizard_form.html"
    file_storage = DefaultStorage()

    def render_done(self, form, **kwargs):
        revalid = True
        return super().render_done(form, **kwargs)

    def get_current_user(self):
        # First step after recaptcha
        step_name = register_form_list[2][0]
        #
        data = self.get_cleaned_data_for_step(step_name)
        if data:
            return User.objects.get(email=data["email"])

        return None

    def process_step(self, form):
        form_data = super().process_step(form)
        step_name = form_data[f"{self.get_prefix(self.request)}-current_step"]
        user = self.get_current_user()

        if isinstance(form, InitialForm) and not user:

            email = form_data[step_name + "-email"]
            # cpf_cnpj = form_data[step_name + "-cpf_cnpj"]
            name = form_data[step_name + "-legal_name"]

            user, created = User.objects.get_or_create(
                username=email,
                email=email,
                first_name=name.split(" ")[0],
                last_name=" ".join(name.split(" ")[:-1]),
            )

            if created:
                user.is_active = False
                user.save()

                send_confirmation_email(
                    user,
                    self.request,
                    email_template_name="candidature/activation_email.html",
                )
                # print("Enviar e-mail")

        if user:
            flow, created = CandidatureFlow.objects.get_or_create(user=user)
            if created and step_name != register_form_list[1][0]:
                for etapa, form in register_form_list:
                    data = self.get_cleaned_data_for_step(etapa)
                    if data:
                        flow.properties.update(
                            dict(
                                (etapa + "-" + key, value)
                                for key, value in data.items()
                            )
                        )

                    if etapa == step_name:
                        break

            flow.properties.update(form_data)
            flow.save()

            # print("Salvando dados")
            # print(flow.properties)
        return form_data

    def process_step_files(self, form):
        return self.get_form_step_files(form)

    def get_template_names(self):
        if self.steps.current == "checkout":
            return "candidature/done.html"
        return super().get_template_names()

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)
        checkout_steps = []
        if self.steps.current == "checkout":
            for step, form_class in self.get_form_list().items():
                if step not in self.steps_hide_on_checkout:
                    data = self.get_cleaned_data_for_step(step)
                    checkout_steps.append(
                        dict(
                            name=step,
                            edit_url=reverse(self.url_name, kwargs={"step": step}),
                            form=form_class(data=data),
                            data=data,
                        )
                    )

            context.update({"checkout_steps": checkout_steps})

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
                elif isinstance(form, ProfileForm):
                    values["video"] = form.cleaned_data.get("video")
                    values["photo"] = form.cleaned_data.get("photo")
                else:
                    values.update(form.cleaned_data)

        # print("---------- Done -----------")
        # print(user.first_name)
        # print(flow.properties)
        # print(values)

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
