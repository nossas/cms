from django.test.client import RequestFactory

from cms.api import add_plugin, create_page
from cms.plugin_rendering import ContentRenderer
from cms.test_utils.testcases import CMSTestCase
from filer.models import File

from ..cms_plugins import CardPlugin

# from .models import Context, Target


# Create your tests here.
class CardPluginsTestCase(CMSTestCase):

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

        self.file = File.objects.create(original_filename="test_image.png", file="test_files/test_image.png")

    def tearDown(self):
        self.home.delete()
        self.superuser.delete()

        if self.file:
            self.file.delete()
            del self.file
            with self.assertRaises(AttributeError):
                print(self.file)
    
    def test_card_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="CardPlugin",
            language=self.language,
        )
        plugin.full_clean()
        self.assertEqual(plugin.plugin_type, "CardPlugin")

    def test_card_plugin_render_html(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="CardPlugin",
            language=self.language,
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = f"""
        <div class="card">
            <div class="card-body"></div>
        </div>
        """

        self.assertHTMLEqual(html, expected_html)

    def test_card_header_plugin_render_html(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="CardPlugin",
            language=self.language,
            header_title="Header title"
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = f"""
        <div class="card">
            <div class="card-header">
                Header title
            </div>
            <div class="card-body"></div>
        </div>
        """

        self.assertHTMLEqual(html, expected_html)

    def test_card_child_plugins(self):
        self.assertEqual(CardPlugin.allow_children, True)
        self.assertEqual(CardPlugin.child_classes, ["TextPlugin", "ButtonPlugin"])


    def test_card_plugin_use_image(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="CardPlugin",
            language=self.language,
            image=self.file
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = f"""
        <div class="card">
            <img src="/media/test_files/test_image.png" class="card-img-top" alt="test_image.png" />
            <div class="card-body"></div>
        </div>
        """

        self.assertHTMLEqual(html, expected_html)