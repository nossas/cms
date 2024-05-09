from django.test.client import RequestFactory

from cms.api import add_plugin, create_page
from cms.plugin_rendering import ContentRenderer
from cms.test_utils.testcases import CMSTestCase

from ..models import NavbarAlignment


# Create your tests here.
class NavbarPluginTestCase(CMSTestCase):

    def setUp(self):
        self.language = "pt-br"
        self.home = create_page(
            title="home", template="ds/base.html", language=self.language
        )
        self.home.is_home = True
        self.home.save()
        
        self.home.publish(self.language)
        self.placeholder = self.home.placeholders.get(slot="content")
        self.superuser = self.get_superuser()

    def tearDown(self):
        self.home.delete()
        self.superuser.delete()

    def test_alignment_content_html(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="NavbarPlugin",
            language=self.language,
            alignment=NavbarAlignment.end,
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = '<div class="collapse navbar-collapse" id="navbarNav" style="justify-content:flex-end"></div>'

        self.assertInHTML(expected_html, html)