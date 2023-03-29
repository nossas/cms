import re

from django.conf import settings
from django.contrib.sites.models import Site
from django.views.defaults import server_error
from django.utils.translation import gettext as _

try:
    # Django > 1.10 uses MiddlewareMixin
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

class DynamicSiteMiddleware(MiddlewareMixin):
    '''
    Routing by domain used to running one server for multiple sites
    '''

    REGEX_PATH_ADMIN = r'/[\w-]*[/]*admin[/]*'

    def process_request(self, request):
        
        host = request.get_host().split(':')[0]

        try:
            current_site = Site.objects.get(domain=host)
        except Site.DoesNotExist:
            match_path = re.match(
                DynamicSiteMiddleware.REGEX_PATH_ADMIN, request.get_full_path())
            
            print(match_path)
            if  match_path is None:
                
                return server_error(request)
            else:
                current_site = Site.objects.get(pk=settings.DEFAULT_SITE_ID)


        request.current_site = current_site
        settings.SITE_ID = current_site.id

        response = self.get_response(request)
        return response