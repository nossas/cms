from django.contrib.sites.models import Site


def ga(request):
    try:
        site = Site.objects.get_current(request)
        if site.ga.uuid:
            return {"ga": site.ga}
    except:
        pass

    return {"ga": None}
