from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def get_uuid_and_token(user):
    return urlsafe_base64_encode(
        force_bytes(user.pk)
    ), default_token_generator.make_token(user)



def send_confirmation_email(user, request, email_template_name):
    uid, token = get_uuid_and_token(user)
    current_site = request.current_site

    activation_url = f'http{"s" if request.is_secure() else ""}://{current_site.domain}{reverse("oauth:change-password", kwargs={"uidb64": uid, "token": token})}'

    subject = "Confirme seu e-mail"
    message = render_to_string(email_template_name, {
        "user": user,
        "activation_url": activation_url
    })
    to_email = user.email
    
    email = EmailMessage(subject, message, to=[to_email])
    email.send()