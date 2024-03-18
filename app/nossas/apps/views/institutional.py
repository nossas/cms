from django.shortcuts import redirect

from cms.utils.urlutils import admin_reverse

from ..models.institutional import InstitutionalInformation


def redirect_add_or_change(request):
    url = admin_reverse("apps_institutionalinformation_add")

    try:
        if request.current_site.institutionalinformation:
            url = admin_reverse(
                "apps_institutionalinformation_change",
                kwargs={"object_id": request.current_site.institutionalinformation.id},
            )
    except InstitutionalInformation.DoesNotExist:
        pass

    return redirect(url)
