from django.shortcuts import render


def override_wizard_create(request):
    import ipdb

    ipdb.set_trace()

    return render(request, template_name="create/index.html")