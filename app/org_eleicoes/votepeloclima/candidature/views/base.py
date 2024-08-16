import hashlib

from django.core.files.storage import default_storage
from django.contrib.auth.models import User, AnonymousUser
from django.urls import reverse

from formtools.wizard.views import NamedUrlSessionWizardView
from contrib.oauth.utils import send_confirmation_email

from ..choices import CandidatureFlowStatus
from ..models import CandidatureFlow, Candidature
from ..forms import register_form_list, ProposeForm, AppointmentForm


def files_is_equal(file1, file2):
    hash1_sha256 = hashlib.sha256()
    for block in iter(lambda: file1.read(4096), b""):
        hash1_sha256.update(block)

    hash2_sha256 = hashlib.sha256()
    for block in iter(lambda: file2.read(4096), b""):
        hash2_sha256.update(block)

    return hash1_sha256.hexdigest() == hash2_sha256.hexdigest()


class CandidatureBaseView(NamedUrlSessionWizardView):
    form_list = register_form_list
    file_storage = default_storage
    template_name = "candidature/wizard_form.html"

    _instance = None

    def get_instance(self):
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

    instance = property(get_instance)

    def render_done(self, form, **kwargs):
        """Válida o captcha respondido na primeira etapa do formulário"""
        revalid = True
        return super().render_done(form, **kwargs)

    def get_current_user(self):
        raise NotImplementedError("Should be implement get_current_user")

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

        if current_step == "informacoes-pessoais" and not user:
            email = form_data[current_step + "-email"]
            name = form_data[current_step + "-legal_name"]

            values = {
                "username": email,
                "email": email,
                "first_name": name.split(" ")[0],
                "last_name": " ".join(name.split(" ")[1:]),
            }
            user, created = User.objects.get_or_create(**values)

            if created:
                user.is_active = False
                user.save()

                send_confirmation_email(user=user, request=self.request)
        
        if user:
            self.upsert_instance(form, current_step, user)
        
        if self.get_next_step(step=current_step) == "checkout":
            self.storage.extra_data["editing"] = True

        return form_data

    def get_form_instance(self, step):
        return self.instance

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

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)
        instance = self.instance

        if hasattr(form.Meta, "title"):
            context.update({"step_title": form.Meta.title})

        if hasattr(form.Meta, "description"):
            context.update({"step_description": form.Meta.description})
        
        if self.steps.next:
            next_form_class = self.get_form_list().get(self.steps.next)
            if hasattr(next_form_class.Meta, "title"):
                context.update({"next_step_title": next_form_class.Meta.title})
        
        if instance and instance.status == "editing":
            context.update({"editing": True})
        
        checkout_steps = []
        if self.steps.current == "checkout":
            user = self.get_current_user()
            instance = CandidatureFlow.objects.get(user=user)

            for step, form_class in self.get_form_list().items():
                if step not in ["captcha", "compromissos"]:
                    checkout_steps.append(dict(
                        name=step,
                        title=getattr(form_class.Meta, "title"),
                        edit_url=reverse("register_step", kwargs={"step": step}),
                        form=form_class(disabled=True, instance=instance)
                    ))
            context.update({"checkout_steps": checkout_steps})
        
        return context
    
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
                return self.render(self.get_form())

        return super().post(*args, **kwargs)
