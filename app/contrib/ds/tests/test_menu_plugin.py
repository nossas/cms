from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware

from cms.api import add_plugin, create_page
from cms.plugin_rendering import ContentRenderer
from cms.test_utils.testcases import CMSTestCase
from cms.toolbar.toolbar import CMSToolbar
from cms.toolbar.utils import get_toolbar_from_request
from sekizai.context import SekizaiContext

from ..models import MenuExtraLink

class MenuPluginTestCase(CMSTestCase):

    def setUp(self):
        self.language = "pt-br"
        self.home = create_page(
            title="home",
            template="ds/base.html",
            language=self.language,
            soft_root=True,
        )
        self.home.is_home = True
        self.home.save()

        self.home.publish(self.language)
        self.placeholder = self.home.placeholders.get(slot="content")
        self.superuser = self.get_superuser()
        self.request_factory = RequestFactory()

    def tearDown(self):
        self.home.delete()
        self.superuser.delete()

    def get_request(self):
        request = self.request_factory.get('/')
        request.user = self.superuser
        request.current_page = self.home

        # Adiciona a sessão ao request
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()

        # Configura a barra de ferramentas do CMS
        toolbar = CMSToolbar(request)
        request.toolbar = toolbar
        return request

    def test_settings_color_menu(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="MenuPlugin",
            language=self.language,
            color="#ffffff",
            attributes={
                "gap": "2",
                "gap_mobile": "1",
                "padding_top": "3",
                "padding_bottom": "4",
            }
        )
        plugin.full_clean()

        request = self.get_request()
        renderer = ContentRenderer(request=request)

        html = renderer.render_plugin(plugin, SekizaiContext())
        expected_html = (
            '<ul id="menu-1" class="navbar-nav" style="--bs-nav-link-color:rgba(255,255,255,1);--bs-nav-link-hover-color:rgba(255,255,255,.75);--bs-navbar-active-color:rgba(255,255,255,.75);padding-top:3rem;padding-bottom:4rem;"></ul>'
        )

        self.assertInHTML(expected_html, html)

    def test_menu_plugin_with_gap_and_padding(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="MenuPlugin",
            language=self.language,
            attributes={
                "gap": "2",
                "gap_mobile": "1",
                "padding_top": "3",
                "padding_bottom": "4",
            }
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, SekizaiContext())
        expected_html = (
            '<ul id="menu-1" class="navbar-nav" style="padding-top:3rem;padding-bottom:4rem;"></ul>'
        )

        self.assertInHTML(expected_html, html)

    def test_render_menu_with_internal_links(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="MenuPlugin",
            language=self.language,
            color="#ffffff",
        )

        self.home.in_navigation = False
        self.home.save()

        internal_link = self.home
        MenuExtraLink.objects.create(internal_link=internal_link, menu_plugin=plugin)

        request = self.get_request()
        renderer = ContentRenderer(request=request)
        html = renderer.render_plugin(plugin, {})
        
        self.assertIn(internal_link.get_absolute_url(), html)

    def test_render_menu_without_internal_links(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="MenuPlugin",
            language=self.language,
            color="#ffffff",
        )

        self.home.in_navigation = True
        self.home.save()

        request = self.get_request()
        renderer = ContentRenderer(request=request)
        html = renderer.render_plugin(plugin, {})
        
        self.assertNotIn('<a href="', html)
