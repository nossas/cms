import mock

from django.conf import settings
from django.contrib.sites.models import Site
from django.http import Http404
from django.test import RequestFactory, TestCase

from backend.middleware import DynamicSiteMiddleware


class DynamicSiteMiddlewareTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        
        Site.objects.create(
            domain="example1.devel",
            name="Example 1"
        )
        Site.objects.create(
            domain="example2.devel",
            name="Example 2"
        )

    def test_change_site_id_settings_by_domain(self):
        get_response = mock.MagicMock()
        request = self.factory.get('/', HTTP_HOST='example2.devel')

        DynamicSiteMiddleware(get_response)(request)

        site = Site.objects.get(domain='example2.devel')

        self.assertEqual(settings.SITE_ID, site.id)
    
    def test_default_site_when_not_found_domain_but_access_admin(self):
        get_response = mock.MagicMock()
        request = self.factory.get('/admin', HTTP_HOST='example3.devel')

        DynamicSiteMiddleware(get_response)(request)

        self.assertEqual(settings.SITE_ID, settings.DEFAULT_SITE_ID)

    def test_500_when_not_found_domain(self):
        get_response = mock.MagicMock()
        request = self.factory.get('/', HTTP_HOST='example3.devel')

        response = DynamicSiteMiddleware(get_response)(request)
        
        self.assertEqual(response.status_code, 500)