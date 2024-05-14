from django.test.client import RequestFactory

from cms.api import add_plugin, create_page
from cms.plugin_rendering import ContentRenderer
from cms.test_utils.testcases import CMSTestCase

from .cms_plugins import AccordionPlugin, AccordionItemPlugin

# from .models import Context, Target


# Create your tests here.
class AccordionPluginsTestCase(CMSTestCase):

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
    
    def test_accordion_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="AccordionPlugin",
            language=self.language,
        )
        plugin.full_clean()
        self.assertEqual(plugin.plugin_type, "AccordionPlugin")

    def test_accordion_plugin_only_accordion_item_child(self):
        self.assertEqual(AccordionPlugin.allow_children, True)
        self.assertEqual(AccordionPlugin.child_classes, ["AccordionItemPlugin"])
    
    def test_accordion_plugin_render_html(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="AccordionPlugin",
            language=self.language,
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = f"""
        <div class="accordion" id="accordion-{plugin.id}">
        </div>
        """

        self.assertHTMLEqual(html, expected_html)

    def test_accordion_item_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="AccordionItemPlugin",
            language=self.language,
        )
        plugin.full_clean()
        self.assertEqual(plugin.plugin_type, "AccordionItemPlugin")

    def test_accordion_item_plugin_only_accordion_parent(self):
        self.assertEqual(AccordionItemPlugin.allow_children, True)
        self.assertEqual(AccordionItemPlugin.require_parent, True)
        self.assertEqual(AccordionItemPlugin.parent_classes, ["AccordionPlugin"])

    def test_accordion_item_plugin_render_html(self):
        target = add_plugin(
            placeholder=self.placeholder,
            plugin_type="CarouselPlugin",
            language=self.language,
        )
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="AccordionItemPlugin",
            language=self.language,
            target=target
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = f"""
        <div class="accordion-item">
            <h2 class="accordion-header">
            <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-{plugin.id}" aria-expanded="true" aria-controls="collapse-{plugin.id}">
                Item {plugin.position}
            </button>
            </h2>
            <div id="collapse-{plugin.id}" class="accordion-collapse collapse" data-bs-parent="#accordion-{target.id}">
                <div class="accordion-body">
                </div>
            </div>
        </div>
        """

        self.assertHTMLEqual(html, expected_html)

    def test_accordion_item_change_header_plugin_render_html(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="AccordionItemPlugin",
            language=self.language,
            header_title="Custom header"
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = f"""
            <h2 class="accordion-header">
            <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-{plugin.id}" aria-expanded="true" aria-controls="collapse-{plugin.id}">
                Custom header
            </button>
            </h2>
        """

        self.assertInHTML(expected_html, html)

    def test_accordion_flush_style_render_html(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="AccordionPlugin",
            language=self.language,
            style="flush"
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = f"""
        <div class="accordion accordion-flush" id="accordion-{plugin.id}">
        </div>
        """

        self.assertHTMLEqual(html, expected_html)

    def test_accordion_grid_layout(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="AccordionPlugin",
            language=self.language,
            grid_columns=3
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = f"""
        <div class="accordion grid" id="accordion-{plugin.id}" style="--bs-columns:3;">
        </div>
        """

        self.assertHTMLEqual(html, expected_html)
    

    def test_accordion_custom_text_colors_and_bacground_colors(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="AccordionPlugin",
            language=self.language,
            text_color="#000",
            bg_color="#fff"
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = f"""
        <div class="accordion" id="accordion-{plugin.id}" style="--bs-body-bg:#fff;--bs-body-color:#000;">
        </div>
        """

        self.assertHTMLEqual(html, expected_html)