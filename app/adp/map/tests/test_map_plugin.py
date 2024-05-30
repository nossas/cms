from django.test.client import RequestFactory
from cms.api import add_plugin, create_page
from cms.plugin_rendering import ContentRenderer
from cms.test_utils.testcases import CMSTestCase

class MapPluginTestCase(CMSTestCase):

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

        self.width="100%",
        self.height="100%",

    def tearDown(self):
        self.home.delete()
        self.superuser.delete()

    def test_map_plugin_render(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="MapPluginPublisher",
            language=self.language,
            url="https://mapa.deolhonasflorestaspublicas.org.br",
            width=self.width,
            height=self.height,
        )
        plugin.full_clean()

        request = RequestFactory().get('/')
        renderer = ContentRenderer(request=request)
        html = renderer.render_plugin(plugin, {})

        expected_html = f'''
        <div style="height:100vh;overflow:hidden">
            <iframe src="https://mapa.deolhonasflorestaspublicas.org.br" width={self.width} height={self.height} frameborder="0" allowfullscreen></iframe>
        </div>'''

        self.assertInHTML(expected_html.strip(), html.strip())
