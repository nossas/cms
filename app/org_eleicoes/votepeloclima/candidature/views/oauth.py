import functools

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy, reverse

from ..models import CandidatureFlow
from ..forms import register_form_list

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