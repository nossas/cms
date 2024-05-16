from django.test.client import RequestFactory
from datetime import date

from cms.api import add_plugin, create_page
from cms.plugin_rendering import ContentRenderer
from cms.test_utils.testcases import CMSTestCase

# from django.template.context import RequestContext
# from sekizai.context import SekizaiContext

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


    # def render_plugin(self, plugin):
    #     request = RequestFactory()
    #     context = SekizaiContext(RequestContext(request))
    #     renderer = ContentRenderer(request)
    #     html = renderer.render_plugin(plugin, context)
    #     return html



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
            <div class="counter-wrapper">
                <span class="counter-number" data-counter></span>
            </div>
        </div>
        """

        self.assertHTMLEqual(html, expected_html)


    def test_counter_plugin_render_html(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="CounterPlugin",
            language=self.language,
            target_number=123
        )
        plugin.full_clean()
        
        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = f"""
        <div id="counter-{plugin.id}" class="counter">
            <div class="counter-wrapper">
                <span class="counter-number" data-counter data-counter-initial="0" data-counter-target="{plugin.target_number}"></span>
            </div>
        </div>
        """

        self.assertHTMLEqual(html, expected_html)


    def test_countup_date(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="CounterPlugin",
            language=self.language,
            initial_date=date(2024, 2, 2),
            target_date=date(2025, 2, 2)
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = f"""
        <div id="counter-{plugin.id}" class="counter">
            <div class="counter-wrapper">
                <span class="counter-number" data-counter data-counter-initial="0" data-counter-target="366"></span>
            </div>
        </div>
        """

        self.assertHTMLEqual(html, expected_html)


    def test_countdown_date(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="CounterPlugin",
            language=self.language,
            initial_date=date(2025, 2, 2),
            target_date=date(2024, 2, 2)
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = f"""
        <div id="counter-{plugin.id}" class="counter">
            <div class="counter-wrapper">
                <span class="counter-number" data-counter data-counter-initial="366" data-counter-target="0"></span>
            </div>
        </div>
        """

        self.assertHTMLEqual(html, expected_html)


    def test_same_initial_and_target_date(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="CounterPlugin",
            language=self.language,
            initial_date=date.today(),
            target_date=date.today()
        )
        plugin.full_clean()
        
        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = f"""
        <div id="counter-{plugin.id}" class="counter">
            <div class="counter-wrapper">
                <span class="counter-number" data-counter data-counter-initial="{plugin.initial_number}" data-counter-end="{plugin.target_date}"></span>
            </div>
        </div>
        """
        self.assertHTMLEqual(html, expected_html)


    def test_description_and_tooltip_render(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="CounterPlugin",
            language=self.language,
            description="Teste Description",
            tooltip_text="Teste Tooltip"
        )
        plugin.full_clean()
        
        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = f"""
        <div id="counter-{plugin.id}" class="counter">
            <div class="counter-wrapper">
                <span class="counter-number" data-counter data-counter-initial="{plugin.initial_number}" data-counter-target="{plugin.target_number}"></span>
            </div>
            <p class="counter-description">{plugin.description}</p>
            <div class="counter-tooltip">
                <span class="counter-tooltip-text">{plugin.tooltip_text}</span>
            </div>
        </div>
        """
        self.assertHTMLEqual(html, expected_html)


    def test_dynamic_number_change(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="CounterPlugin",
            language=self.language,
            initial_number=100,
            target_number=200
        )
        plugin.full_clean()
        plugin.target_number = 300
        plugin.save()

        
        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = f"""
        <div id="counter-{plugin.id}" class="counter">
            <div class="counter-wrapper">
                <span class="counter-number" data-counter data-counter-initial="{plugin.initial_number}" data-counter-target="{plugin.target_number}"></span>
            </div>
        </div>
        """
        self.assertHTMLEqual(html, expected_html)
