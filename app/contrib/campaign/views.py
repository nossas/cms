import json
from django.shortcuts import render
from django.http import JsonResponse

from .forms import PressureForm

# Create your views here.


def override_wizard_create(request):
    import ipdb

    ipdb.set_trace()

    return render(request, template_name="create/index.html")


def pressure_submit_ajax(request):
    if request.method == "POST":
        data = json.loads(request.body)
        form = PressureForm(data)

        if form.is_valid():
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "error", "errors": form.errors})
