from django.test.client import RequestFactory

from cms.api import add_plugin, create_page
from cms.plugin_rendering import ContentRenderer
from cms.test_utils.testcases import CMSTestCase

from contrib.ds.tests.helpers import get_filer_image


class ImagePluginTestCase(CMSTestCase):

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

        self.image = get_filer_image()

    def tearDown(self):
        self.home.delete()
        self.superuser.delete()

        if self.image:
            self.image.delete()
            del self.image
            with self.assertRaises(AttributeError):
                print(self.image)

    def test_image_plugin_responsive(self):        
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="PicturePlugin",
            language=self.language,
            picture=self.image,
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())
        html = renderer.render_plugin(plugin, {})
        
        expected_html = 'class="img-fluid "'
        assert expected_html in html

    def test_image_plugin_not_responsive(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="PicturePlugin",
            language=self.language,
            picture=self.image,
            use_responsive_image='no',  # Explicitly set to 'no'
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())
        html = renderer.render_plugin(plugin, {})

        unexpected_html = 'class="img-fluid "'
        assert unexpected_html not in html

    def test_image_plugin_with_custom_classes(self):
        attributes = {'class': 'custom-class'}
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="PicturePlugin",
            language=self.language,
            picture=self.image,
            attributes=attributes,
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())
        html = renderer.render_plugin(plugin, {})

        expected_html = 'class="img-fluid custom-class"'
        assert expected_html in html