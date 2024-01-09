# from django.contrib import admin
from django.shortcuts import redirect
# from django.urls import path

from cms.utils.urlutils import admin_reverse    

from .models import InstitutionalInformation


def redirect_add_or_change(request):
    url = admin_reverse("institutional_institutionalinformation_add")

    try:
        if request.current_site.institutionalinformation:
            url = admin_reverse(
                "institutional_institutionalinformation_change",
                kwargs={"object_id": request.current_site.institutionalinformation.id},
            )
    except InstitutionalInformation.DoesNotExist:
            pass
    
    return redirect(url)