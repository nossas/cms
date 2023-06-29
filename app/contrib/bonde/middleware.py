from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.contrib.sites.models import Site

from django.http import Http404


class SiteMiddleware(MiddlewareMixin):
    
    def process_request(self, request):
        try:
            current_site = Site.objects.get(domain=request.get_host())
        except Site.DoesNotExist:
            # current_site = Site.objects.get(id=settings.DEFAULT_SITE_ID)
            raise Http404

        request.current_site = current_site
        
        settings.SITE_ID = current_site.id