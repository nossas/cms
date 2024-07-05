from django.shortcuts import render, redirect
from django.urls import reverse
from formtools.wizard.views import NamedUrlCookieWizardView

from .forms import register_form_list


class RegisterView(NamedUrlCookieWizardView):
    form_list = register_form_list
    steps_hide_on_checkout = ['captcha']

    def render_done(self, form, **kwargs):
        revalid = True
        return super().render_done(form, **kwargs)

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
                if step in ('sobre-sua-trajetoria', 'bandeiras-da-sua-candidatura', 'compromissos'):
                    import ipdb;ipdb.set_trace()

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
        print("---------- Done -----------")
        # print(form_dict)
        # checkout_steps = []
        # for key, value in form_dict.items():
        #     checkout_steps.append(
        #         dict(
        #             edit_url=reverse("register_step", kwargs={"step": key}), form=value
        #         )
        #     )

        # return render(
        #     self.request, "candidature/done.html", {"checkout_steps": checkout_steps}
        # )
        return redirect("/")
