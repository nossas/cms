from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect


class EleicaoRedirectMiddleware(MiddlewareMixin):
    domain = "aeleicaodoano.org"
    redirect_domains = ["aeleicaodoano.com"]

    def process_request(self, request):
        host = request.get_host().partition(":")[0]

        if host in self.redirect_domains:
            return HttpResponsePermanentRedirect(f"https://{self.domain}" + request.path)
