import datetime

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from formtools.wizard.views import NamedUrlSessionWizardView

from .models import CandidatureFlow, CandidatureFlowStatus, Candidature
from .forms import register_form_list, InitialForm, FlagForm, AppointmentForm


class RegisterView(NamedUrlSessionWizardView):
    form_list = register_form_list
    steps_hide_on_checkout = ["captcha"]

    def render_done(self, form, **kwargs):
        revalid = True
        return super().render_done(form, **kwargs)

    def get_current_user(self):
        # First step after recaptcha
        step_name = register_form_list[1][0]
        #
        data = self.get_cleaned_data_for_step(step_name)
        if data:
            return User.objects.get(email=data["email"])

        return None

    def process_step(self, form):
        form_data = super().process_step(form)

        step_name = form_data["register_view-current_step"]
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
                print("Enviar e-mail")

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
                            edit_url=reverse("register_step", kwargs={"step": step}),
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
            if step not in self.steps_hide_on_checkout and step != 'checkout':
                if isinstance(form, FlagForm):
                    values.update({"flags": form.cleaned_data})
                elif isinstance(form, AppointmentForm):
                    values.update({"appointments": form.cleaned_data})
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
