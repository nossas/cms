import json

from datetime import datetime
from functools import reduce
from collections import OrderedDict
# from typing import TypedDict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator

from contrib.oauth.mixins import JsonLoginRequiredMixin

from ..choices import CandidatureFlowStatus
from ..models import CandidatureFlow, Candidature
from ..forms import register_form_list, ProposeForm, AppointmentForm

disable_edit_steps = [
    "informacoes-pessoais",
    "informacoes-de-candidatura",
    "captcha",
    "compromissos",
]


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

                checkout_steps.append(step_dict)

        return checkout_steps

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.request.user.is_staff:
            flow = self.request.user.candidatureflow
            checkout_steps = self.get_checkout_steps()
            is_valid = reduce(
                lambda x, y: x and y,
                list(map(lambda x: x.get("is_valid"), checkout_steps)),
            )

            context.update(
                {
                    "flow": flow,
                    "checkout_steps": checkout_steps,
                    "checkout_is_valid": is_valid,
                    "is_public": flow.status
                    in [CandidatureFlowStatus.is_valid, CandidatureFlowStatus.editing]
                    and flow.candidature,
                }
            )

        return context

    def post(self, request, *args, **kwargs):
        if "request_change" in request.POST:
            flow = request.user.candidatureflow
            flow.status = CandidatureFlowStatus.editing
            flow.save()

            return redirect(reverse("register_step", kwargs={"step": "checkout"}))

        return super().post(request, *args, **kwargs)


# Validation = TypedDict("Validation", {
#     "status": str,
#     "slug": str,
#     "name": str,
#     "content": str | None
# })


@method_decorator(csrf_exempt, name="dispatch")
class UpdateCandidatureStatusView(JsonLoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        validation = json.loads(request.body)
        instance = CandidatureFlow.objects.get(user=request.user)
        instance.validations = instance.validations or {}

        if instance.status == "submitted" and validation.get("status") == "validating":
            instance.validations.update({
                validation.get("slug"): {
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "content": validation.get("content"),
                    "name": validation.get("name"),
                    "status": CandidatureFlowStatus.is_valid
                }
            })
            
            instance.save()
        elif instance.status == "submitted" and validation.get("status") == CandidatureFlowStatus.invalid:
            instance.validations.update({
                validation.get("slug"): {
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "content": validation.get("content"),
                    "name": validation.get("name"),
                    "status": CandidatureFlowStatus.invalid
                }
            })

            instance.status = CandidatureFlowStatus.invalid
            instance.save()

            return JsonResponse({"message": "fail"}, status=200)
        elif instance.status == "submitted" and validation.get("status") == CandidatureFlowStatus.is_valid:
            instance.validations.update({
                validation.get("slug"): {
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "content": validation.get("content"),
                    "name": validation.get("name"),
                    "status": CandidatureFlowStatus.is_valid
                }
            })

            instance.status = CandidatureFlowStatus.is_valid

            values = {}
            for step, form_class in OrderedDict(register_form_list).items():
                if step not in ("captcha", "checkout"):
                    form = form_class(
                        instance=CandidatureFlow.objects.get(user=request.user),
                        data=instance.properties,
                    )
                    if form.is_valid():
                        if isinstance(form, ProposeForm):
                            # TODO: Mudar depois de mergear para proposes
                            values.update(
                                {"proposes": form.cleaned_data.get("properties")}
                            )
                        elif isinstance(form, AppointmentForm):
                            values.update(
                                {"appointments": form.cleaned_data.get("properties")}
                            )
                        else:
                            cleaned = form.cleaned_data.copy()
                            properties = cleaned.pop("properties", {})
                            values.update({**properties, **cleaned})

            if instance.candidature:
                Candidature.objects.filter(id=instance.candidature.id).update(**values)
            else:
                instance.candidature = Candidature.objects.create(**values)
            
            instance.save()

        return JsonResponse({"message": "success"}, status=200)
