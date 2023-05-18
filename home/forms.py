from django import forms


def unzip_widget(label, Widget = forms.TextInput, **extra_attrs):
    if not extra_attrs:
        extra_attrs = dict()

    extra_widget_attrs = extra_attrs.pop('widget_attrs', None)

    widget = Widget(attrs={"class": "form-control", "placeholder": label})
    
    if extra_widget_attrs:
        widget = Widget(
            attrs={"class": "form-control", "placeholder": label},
            **extra_widget_attrs
        )

    extra_attrs.update({
        "label": label,
        "widget": widget
    })

    return extra_attrs


class PersonFormMixin(forms.Form):
    given_name = forms.CharField(**unzip_widget("Primeiro nome"))
    family_name = forms.CharField(**unzip_widget("Sobrenome"), required=False)
    email_address = forms.EmailField(**unzip_widget("Seu melhor e-mail", Widget=forms.EmailInput))
    phone_number = forms.CharField(**unzip_widget("Número de telefone"))


class PressureForm(PersonFormMixin):
    email_subject = forms.CharField(**unzip_widget("Assunto"))
    email_body = forms.CharField(**unzip_widget("Corpo do e-mail", Widget=forms.Textarea))

    template_name = "home/components/form.html"



class LoggedPressureForm(forms.Form):
    person_id = forms.CharField(**unzip_widget("Pessoa", Widget=forms.HiddenInput))

    email_subject = forms.CharField(**unzip_widget("Assunto"))
    email_body = forms.CharField(**unzip_widget("Corpo do e-mail", Widget=forms.Textarea))

    template_name = "home/components/form.html"