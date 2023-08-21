from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponsePermanentRedirect


class WwwRedirectMiddleware(MiddlewareMixin):
    def process_request(self, request):
        host = request.get_host().partition(":")[0]

        if host.startswith("www"):
            domain = host.split("www.")[1]

            return HttpResponsePermanentRedirect(f"https://{domain}" + request.path)
