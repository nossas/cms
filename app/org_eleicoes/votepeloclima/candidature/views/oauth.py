import functools

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
from ..forms import register_form_list, ProposeForm, TrackForm, ProfileForm

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
            checkout_steps = self.get_checkout_steps()
            is_valid = functools.reduce(lambda x, y: x and y, list(map(lambda x: x.get("is_valid"), checkout_steps)))
            # checkout_steps = []
            context.update(
                {
                    "flow": self.request.user.candidatureflow,
                    "checkout_steps": checkout_steps,
                    "checkout_is_valid": is_valid
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


@method_decorator(csrf_exempt, name='dispatch')
class UpdateCandidatureStatusView(JsonLoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        instance = request.user.candidatureflow
        if instance.status == "submitted":
            values = {}
            for form_class in (ProposeForm, TrackForm, ProfileForm):
                instance = CandidatureFlow.objects.get(user=request.user)
                form = form_class(instance=instance, data=instance.properties)
                if form.is_valid():
                    if isinstance(form, ProposeForm):
                        values.update({"flags": form.cleaned_data.get("properties")})
                    else:
                        cleaned = form.cleaned_data.copy()
                        properties = cleaned.pop("properties", {})
                        values.update({**properties, **cleaned})
            
            import ipdb;ipdb.set_trace()
            if instance.candidature:
                Candidature.objects.filter(id=instance.candidature.id).update(**values)
                instance.status = "success"
                instance.save()
            else:
                instance.candidature = Candidature.objects.create(**values)
                instance.status = "success"
                instance.save()

        return JsonResponse({"message": "success"})