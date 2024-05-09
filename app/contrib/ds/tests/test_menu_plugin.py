from django.test.client import RequestFactory

from cms.api import add_plugin, create_page
from cms.plugin_rendering import ContentRenderer
from cms.test_utils.testcases import CMSTestCase


# Create your tests here.
class MenuPluginTestCase(CMSTestCase):

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

    def test_settings_color_menu(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="MenuPlugin",
            language=self.language,
            color="#ffffff",
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = '<ul class="navbar-nav" style="--bs-nav-link-color:rgba(255,255,255,1);--bs-nav-link-hover-color:rgba(255,255,255,.75)"></ul>'

        self.assertInHTML(expected_html, html)