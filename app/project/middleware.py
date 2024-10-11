from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponsePermanentRedirect
from django.conf import settings


class WwwRedirectMiddleware(MiddlewareMixin):
    def process_request(self, request):
        host = request.get_host().partition(":")[0]

        if host.startswith("www"):
            domain = host.split("www.")[1]

            return HttpResponsePermanentRedirect(f"https://{domain}" + request.path)


class DomainRedirectMiddleware(MiddlewareMixin):

    def process_request(self, request):
        host = request.get_host().partition(":")[0]

        if host in self.redirect_domains:
            return HttpResponsePermanentRedirect(
                f"https://{self.domain}" + request.path
            )

    @property
    def domain(self):
        return getattr(settings, "REDIRECT_MIDDLEWARE_ROOT_DOMAIN", "")

    @property
    def redirect_domains(self):
        return getattr(settings, "REDIRECT_MIDDLEWARE_LIST_DOMAIN", [])
