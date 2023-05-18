from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User

from .forms import PressureForm


def action_form_view(request):
    if request.method == "POST":

        form = PressureForm(request.POST)
        if form.is_valid():
            user, created = User.objects.get_or_create(
                username=form.cleaned_data['email_address'],
                email=form.cleaned_data['email_address'],
                first_name=form.cleaned_data['given_name'],
                last_name=form.cleaned_data['family_name'],
                is_staff=False
            )

            login(request, user)
            request.session.set_expiry(0)
    else:
        form = PressureForm()
    
    return render(request, 'home/action_page.html', {'form': form})


def logout_view(request):
    import ipdb;ipdb.set_trace()
    logout(request)
    
    return HttpResponseRedirect(request.path)