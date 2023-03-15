from django.contrib import messages
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import FormView

from .forms import FormBuilder
from .models import Form
from .utils import hashid_to_int


# class FormSubmission(FormView):
#     form_class = FormBuilder
#     http_method_names = ['post']

#     def get_form_kwargs(self):
#         form_kwargs = super(FormSubmission, self).get_form_kwargs()
#         form_id = hashid_to_int(self.request.POST['form_id'])
#         form_instance = get_object_or_404(Form, pk=form_id)
#         form_kwargs.update({
#             'form_instance': form_instance
#         })

#         import ipdb; ipdb.set_trace()
#         return form_kwargs

#     def form_valid(self, form, *args, **kwargs):
#         import ipdb; ipdb.set_trace()
#         form.save(request=self.request)

#         if self.request.is_ajax():
#             response = {
#                 'formIsValid': True
#             }
#             return JsonResponse(response)
#         else:
#             messages.success(self.request, 'Submit com sucesso!')

#             return redirect('/')
    
#     def form_invalid(self, form, *args, **kwargs):
#         import ipdb; ipdb.set_trace()
#         if self.request.is_ajax():
#             response = {
#                 'formIsValid': False,
#                 'errors': form.errors,
#             }
#             return JsonResponse(response)
#         else:
#             redirect_url = form.cleaned_data.get('referrer') or self.request.META.get('HTTP_REFERER', '')
#             # if is_safe_url(redirect_url, self.request.get_host()):
#             #     messages.error(self.request, _(u'Invalid form data, one or more fields had errors'))
#             #     return redirect(redirect_url)

#             # If for some reason someone was manipulated referrer parameter to
#             # point to unsafe URL then we will raise Http404 as we do with invalid form_id
#             raise Http404('Invalid referrer')

def submit_form_json(request):
    if request.method == 'POST':
        form_id = hashid_to_int(request.POST['form_id'])
        form_instance = Form.objects.get(pk=form_id)

        form = FormBuilder(
            initial={'referrer': request.path_info},
            form_instance=form_instance,
            data=request.POST,
            label_suffix='',
            auto_id='%s'
        )

        if form.is_valid():
            # import ipdb; ipdb.set_trace()
            return JsonResponse({ 'formIsValid': True })
        else:
            # import ipdb; ipdb.set_trace()
            return JsonResponse({ 'formIsValid': False, 'errors': form.errors })