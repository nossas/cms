import hashlib

from django.core.files.storage import default_storage
from django.contrib.auth.models import User, AnonymousUser

from formtools.wizard.views import NamedUrlSessionWizardView
from contrib.oauth.utils import send_confirmation_email

from ..models import CandidatureFlow
from ..forms import register_form_list


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

    # def render_done(self, form, **kwargs):
    #     revalid = True
    #     return super().render_done(form, **kwargs)

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

        return form_data

    def get_form_instance(self, step):
        return self.instance