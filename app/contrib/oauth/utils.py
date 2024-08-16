from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .forms import OAuthPasswordResetForm


def get_uuid_and_token(user):
    return urlsafe_base64_encode(
        force_bytes(user.pk)
    ), default_token_generator.make_token(user)



def send_confirmation_email(
    user,
    request,
    from_email=None,
    subject_template_name="oauth/email/password_reset_subject.txt",
    email_template_name="oauth/email/password_reset_confirm.html"
):
    opts = {
        "use_https": request.is_secure(),
        "token_generator": default_token_generator,
        "request": request,
        "from_email": from_email,
        "subject_template_name": subject_template_name,
        "email_template_name": email_template_name,
        "extra_email_context": {}
    }

    form = OAuthPasswordResetForm(data={"email": user.email})
    if form.is_valid():
        form.save(**opts)
