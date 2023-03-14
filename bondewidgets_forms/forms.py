from django import forms
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from unidecode import unidecode

from .utils import int_to_hashid
from .widgets import DateInput, TelephoneInput, TimeInput
from .models import FormField


class FormBuilder(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'

    form_id = forms.CharField(widget=forms.HiddenInput)
    referrer = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, form_instance, *args, **kwargs):
        super(FormBuilder, self).__init__(*args, **kwargs)
        self.form_instance = form_instance
        self.field_names = []
        self.file_fields = []
        self.field_types = {}

        # self.submission_url = reverse('djangocms_forms_submissions')
        self.fields['form_id'].initial = int_to_hashid(form_instance.pk)
        # self.redirect_url = form_definition.redirect_url

        for field in form_instance.fields.all():
            if hasattr(self, 'prepare_%s' % field.field_type):
                field_name = self.get_unique_field_name(field)
                form_field = getattr(self, 'prepare_%s' % field.field_type)(field)

                self.fields[field_name] = form_field

                # if isinstance(form_field, FormBuilderFileField):
                #     self.file_fields.append(field_name)

        # if form_definition.use_honeypot:
        #     self.fields['__toc__'] = HoneyPotField()
        # elif form_definition.use_recaptcha:
        #     field_name = 'recaptcha_%s' % int_to_hashid(form_definition.pk, min_length=8)
        #     self.fields[field_name] = ReCaptchaField(label=_('Are you a robot?'))

    def get_unique_field_name(self, field):
        field_name = field.field_name or field.label
        field_name = '%s' % (slugify(unidecode(field_name).replace('-', '_')))

        if field_name in self.field_names:
            i = 1
            while True:
                if i > 1:
                    if i > 2:
                        field_name = field_name.rsplit('_', 1)[0]
                    field_name = '%s_%s' % (field_name, i)
                if field_name not in self.field_names:
                    break
                i += 1

        self.field_names.append(field_name)
        self.field_types[field_name] = field.field_type
        return field_name

    def split_choices(self, choices):
        return [x.strip() for x in choices.split(',') if x.strip()]

    def to_bool(self, value):
        return value.lower() in ('yes', 'y', 'true', 't', '1')

    def prepare_text(self, field):
        field_attrs = field.build_field_attrs()
        widget_attrs = field.build_widget_attrs()

        field_attrs.update({
            'widget': forms.TextInput(attrs=widget_attrs)
        })
        return forms.CharField(**field_attrs)

    def prepare_textarea(self, field):
        field_attrs = field.build_field_attrs()
        widget_attrs = field.build_widget_attrs()

        field_attrs.update({
            'widget': forms.Textarea(attrs=widget_attrs)
        })
        return forms.CharField(**field_attrs)

    def prepare_email(self, field):
        field_attrs = field.build_field_attrs()
        widget_attrs = field.build_widget_attrs(extra_attrs={'autocomplete': 'email'})

        field_attrs.update({
            'widget': forms.EmailInput(attrs=widget_attrs),
        })
        return forms.EmailField(**field_attrs)

    def prepare_checkbox(self, field):
        field_attrs = field.build_field_attrs()
        widget_attrs = field.build_widget_attrs()

        field_attrs.update({
            'widget': forms.CheckboxInput(attrs=widget_attrs)
        })

        if field.initial:
            field_attrs.update({
                'initial': self.to_bool(field.initial)
            })
        return forms.BooleanField(**field_attrs)

    def prepare_checkbox_multiple(self, field):
        field_attrs = field.build_field_attrs()
        widget_attrs = field.build_widget_attrs()

        field_attrs.update({
            'widget': forms.CheckboxSelectMultiple(attrs=widget_attrs),
            'choices': field.get_choices(),
        })

        if field.initial:
            field_attrs.update({
                'initial': self.split_choices(field.initial)
            })
        return forms.MultipleChoiceField(**field_attrs)

    def prepare_select(self, field):
        field_attrs = field.build_field_attrs()
        widget_attrs = field.build_widget_attrs()

        field_attrs.update({
            'widget': forms.Select(attrs=widget_attrs)
        })

        if field.choice_values:
            choice_list = field.get_choices()
            if not field.required:
                choice_list.insert(0, ('', field.placeholder_text or _('Please select an option')))
            field_attrs.update({
                'choices': choice_list
            })
        return forms.ChoiceField(**field_attrs)

    def prepare_radio(self, field):
        field_attrs = field.build_field_attrs()
        widget_attrs = field.build_widget_attrs()

        field_attrs.update({
            'widget': forms.RadioSelect(attrs=widget_attrs),
            'choices': field.get_choices(),
        })
        return forms.ChoiceField(**field_attrs)

    # def prepare_file(self, field):
    #     field_attrs = field.build_field_attrs()
    #     widget_attrs = field.build_widget_attrs()

    #     field_attrs.update({
    #         'widget': forms.ClearableFileInput(attrs=widget_attrs)
    #     })

    #     if field.choice_values:
    #         regex = re.compile('[\s]*\n[\s]*')
    #         choices = regex.split(field.choice_values)
    #         field_attrs.update({
    #             'allowed_file_types': [i.lstrip('.').lower() for i in choices]
    #         })
    #     return FormBuilderFileField(**field_attrs)

    def prepare_date(self, field):
        field_attrs = field.build_field_attrs()
        widget_attrs = field.build_widget_attrs()

        field_attrs.update({
            'widget': DateInput(attrs=widget_attrs),
        })
        return forms.DateField(**field_attrs)

    def prepare_time(self, field):
        field_attrs = field.build_field_attrs()
        widget_attrs = field.build_widget_attrs()

        field_attrs.update({
            'widget': TimeInput(attrs=widget_attrs),
        })
        return forms.TimeField(**field_attrs)

    def prepare_hidden(self, field):
        field_attrs = field.build_field_attrs()
        widget_attrs = field.build_widget_attrs()

        field_attrs.update({
            'widget': forms.HiddenInput(attrs=widget_attrs),
        })
        return forms.CharField(**field_attrs)

    def prepare_number(self, field):
        field_attrs = field.build_field_attrs()
        widget_attrs = field.build_widget_attrs()

        field_attrs.update({
            'widget': forms.NumberInput(attrs=widget_attrs)
        })
        return forms.IntegerField(**field_attrs)

    def prepare_url(self, field):
        field_attrs = field.build_field_attrs()
        widget_attrs = field.build_widget_attrs()

        field_attrs.update({
            'widget': forms.URLInput(attrs=widget_attrs)
        })
        return forms.URLField(**field_attrs)

    def prepare_password(self, field):
        field_attrs = field.build_field_attrs()
        widget_attrs = field.build_widget_attrs()

        field_attrs.update({
            'widget': forms.PasswordInput(attrs=widget_attrs),
        })
        return forms.CharField(**field_attrs)

    def prepare_phone(self, field):
        field_attrs = field.build_field_attrs()
        widget_attrs = field.build_widget_attrs()

        field_attrs.update({
            'widget': TelephoneInput(attrs=widget_attrs),
        })
        return forms.CharField(**field_attrs)


class FieldForm(forms.ModelForm):
    class Meta:
        model = FormField
        fields = '__all__'
    
 