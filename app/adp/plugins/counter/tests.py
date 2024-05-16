from django.test.client import RequestFactory
from datetime import date

from cms.api import add_plugin, create_page
from cms.plugin_rendering import ContentRenderer
from cms.test_utils.testcases import CMSTestCase
from filer.models import File

from .cms_plugins import CounterPlugin

# from .models import Context, Target


# Create your tests here.
class CounterPluginTestCase(CMSTestCase):

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

    
    def test_counter_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="CounterPlugin",
            language=self.language,
        )
        plugin.full_clean()
        self.assertEqual(plugin.plugin_type, "CounterPlugin")

    def test_counter_plugin_render_html(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="CounterPlugin",
            language=self.language,
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = f"""
        <div id="counter-{plugin.id}" class="counter">
            <div class="counter-number"></div>
        </div>
        """

        self.assertHTMLEqual(html, expected_html)

    def test_counter_plugin_render_html(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="CounterPlugin",
            language=self.language,
            end_number=123
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = f"""
        <div id="counter-{plugin.id}" class="counter">
            <div class="counter-number" data-counter data-counter-start="0" data-counter-end="{plugin.end_number}">
            </div>
        </div>
        """

        self.assertHTMLEqual(html, expected_html)

    def test_countup_date(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="CounterPlugin",
            language=self.language,
            start_date=date(2024, 2, 2),
            end_date=date(2025, 2, 2)
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = f"""
        <div id="counter-{plugin.id}" class="counter">
            <div class="counter-number" data-counter data-counter-start="0" data-counter-end="366">
            </div>
        </div>
        """

        self.assertHTMLEqual(html, expected_html)


    def test_countdown_date(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="CounterPlugin",
            language=self.language,
            start_date=date(2025, 2, 2),
            end_date=date(2024, 2, 2)
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = f"""
        <div id="counter-{plugin.id}" class="counter">
            <div class="counter-number" data-counter data-counter-start="366" data-counter-end="0">
            </div>
        </div>
        """

        self.assertHTMLEqual(html, expected_html)