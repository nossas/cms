from collections import OrderedDict
from django.contrib.auth.models import User
from django.shortcuts import render

from .base import CandidatureBaseView
from ..choices import CandidatureFlowStatus
from ..forms import ProposeForm, AppointmentForm
from ..models import Candidature, CandidatureFlow


class CreateUpdateCandidatureView(CandidatureBaseView):
    
    def get_current_user(self):
        data = self.get_cleaned_data_for_step("informacoes-pessoais")
        user = self.request.user if isinstance(self.request.user, User) else None

        if data and not user:
            return User.objects.get(email=data["properties"]["email"])
        
        return user

    def render_done(self, form, **kwargs):
        """
        This method gets called when all forms passed. The method should also
        re-validate all steps to prevent manipulation. If any form fails to
        validate, `render_revalidation_failure` should get called.
        If everything is fine call `done`.
        """
        final_forms = OrderedDict()
        # walk through the form list and try to validate the data again.
        for form_key in self.get_form_list():
            form_obj = self.get_form(
                step=form_key,
                data=self.storage.get_step_data(form_key),
                files=self.storage.get_step_files(form_key)
            )
            if not form_obj.is_valid() and self.instance.status == "draft":  # Revalidation only draft
                return self.render_revalidation_failure(form_key, form_obj, **kwargs)
            final_forms[form_key] = form_obj

        # render the done view and reset the wizard before returning the
        # response. This is needed to prevent from rendering done with the
        # same data twice.
        done_response = self.done(list(final_forms.values()), form_dict=final_forms, **kwargs)
        self.storage.reset()
        return done_response

    def done(self, form_list, form_dict, **kwargs):
        user = self.get_current_user()
        flow = CandidatureFlow.objects.get(user=user)
        flow.status = CandidatureFlowStatus.submitted
        flow.save()
        
        # Submete Editing
        print("Enviar e-mail de cadastro enviado")

        return render(self.request, "candidature/submitted.html")