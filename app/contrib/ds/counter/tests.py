from django.test.client import RequestFactory
from datetime import date

from cms.api import add_plugin, create_page
from cms.plugin_rendering import ContentRenderer
from cms.test_utils.testcases import CMSTestCase

from sekizai.context import SekizaiContext

from contrib.ds.counter.cms_plugins import CounterPlugin


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

        html = renderer.render_plugin(plugin, SekizaiContext())
        expected_html = f"""
        <span data-counter></span>
        """

        self.assertHTMLEqual(html, expected_html)

    def test_counter_plugin_render_html(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="CounterPlugin",
            language=self.language,
            target_number=123,
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, SekizaiContext())
        expected_html = f"""
        <span data-counter data-counter-initial="0" data-counter-target="{plugin.target_number}">0</span>
        """

        self.assertHTMLEqual(html, expected_html)

    def test_countup_date(self):
        target_date = date(2023, 1, 1)

        target_days = (date.today() - target_date).days

        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="CounterPlugin",
            language=self.language,
            target_date=target_date,
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, SekizaiContext())
        expected_html = f"""
        <span data-counter data-counter-initial="0" data-counter-target="{target_days}">0</span>
        """

        self.assertHTMLEqual(html, expected_html)

    def test_countdown_date(self):
        initial_date = date(2024, 1, 2)
        target_date = date(2024, 2, 2)

        target_days = (target_date - date.today()).days

        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="CounterPlugin",
            language=self.language,
            initial_date=initial_date,
            target_date=target_date,
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, SekizaiContext())
        expected_html = f"""
        <span data-counter data-counter-initial="31" data-counter-target="{target_days}">0</span>
        """

        self.assertHTMLEqual(html, expected_html)

    def test_dynamic_number_change(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="CounterPlugin",
            language=self.language,
            initial_number=0,
            target_number=200,
        )
        plugin.full_clean()
        plugin.target_number = 300
        plugin.save()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, SekizaiContext())
        expected_html = f"""
        <span data-counter data-counter-initial="{plugin.initial_number}" data-counter-target="{plugin.target_number}">0</span>
        """
        self.assertHTMLEqual(html, expected_html)

    def test_counter_render_children(self):
        self.assertEqual(CounterPlugin.allow_children, True)

    def test_counter_text_enabled(self):
        self.assertEqual(CounterPlugin.text_enabled, True)