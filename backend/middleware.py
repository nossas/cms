from django.conf import settings
from django.contrib.sites.models import Site

try:
    # Django > 1.10 uses MiddlewareMixin
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

class DynamicSiteMiddleware(MiddlewareMixin):
    '''
    Routing by domain used to running one server for multiple sites
    '''

    def process_request(self, request):
        host = request.get_host().split(':')[0]

        try:
            current_site = Site.objects.get(domain=host)
        except Site.DoesNotExist:
            current_site = Site.objects.get(id=settings.DEFAULT_SITE_ID)

        request.current_site = current_site
        settings.SITE_ID = current_site.id

        response = self.get_response(request)
        return response