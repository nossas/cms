from django.test.client import RequestFactory

from cms.api import add_plugin, create_page
from cms.plugin_rendering import ContentRenderer
from cms.test_utils.testcases import CMSTestCase

from ..cms_plugins import CarouselPlugin, CarouselContentPlugin

# from .models import Context, Target


# Create your tests here.
class CarouselPluginsTestCase(CMSTestCase):

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

    def test_carousel_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="CarouselPlugin",
            language=self.language,
        )
        plugin.full_clean()
        self.assertEqual(plugin.plugin_type, "CarouselPlugin")

    def test_carousel_plugin_add_children_only_content(self):
        self.assertEqual(CarouselPlugin.allow_children, True)
        self.assertEqual(CarouselPlugin.child_classes, ["CarouselContentPlugin"])

    def test_carousel_content_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="CarouselContentPlugin",
            language=self.language,
        )
        plugin.full_clean()
        self.assertEqual(plugin.plugin_type, "CarouselContentPlugin")
        self.assertEqual(CarouselContentPlugin.allow_children, True)

    def test_carousel_content_parent_only_carousel_plugin(self):
        self.assertEqual(CarouselContentPlugin.parent_classes, ["CarouselPlugin"])

    # def test_carousel_plugin_unique_id_render_html(self):
    #     plugin = add_plugin(
    #         placeholder=self.placeholder,
    #         plugin_type="CarouselPlugin",
    #         language=self.language,
    #     )
    #     plugin.full_clean()

    #     renderer = ContentRenderer(request=RequestFactory())

    #     html = renderer.render_plugin(plugin, {})

    #     self.assertInHTML('<div id="carousel-{plugin.id}" class="carousel slide">', html)

    def test_carousel_plugin_inner_render_html(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="CarouselPlugin",
            language=self.language,
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = """
        <div class="carousel-inner">
        </div>
        """

        self.assertInHTML(expected_html, html)

    def test_carousel_plugin_unique_id_target_controls_render_html(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="CarouselPlugin",
            language=self.language,
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = f"""
        <button class="carousel-control-prev" type="button" data-bs-target="#carousel-{plugin.id}" data-bs-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Previous</span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#carousel-{plugin.id}" data-bs-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Next</span>
        </button>
        """

        self.assertInHTML(expected_html, html)

    def test_carousel_content_plugin_render_html(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="CarouselContentPlugin",
            language=self.language,
        )
        plugin.full_clean()

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = "<div class='carousel-item active'></div>"

        self.assertHTMLEqual(html, expected_html)

    def test_first_carousel_content_active(self):
        target = add_plugin(
            placeholder=self.placeholder,
            plugin_type="CarouselPlugin",
            language=self.language,
        )
        plugin1 = add_plugin(
            placeholder=self.placeholder,
            plugin_type="CarouselContentPlugin",
            language=self.language,
            target=target,
        )
        plugin2 = add_plugin(
            placeholder=self.placeholder,
            plugin_type="CarouselContentPlugin",
            language=self.language,
            target=target,
        )

        plugin_instance = plugin1.get_plugin_class_instance()
        context = plugin_instance.render({}, plugin1, None)

        self.assertIn("is_active", context)
        self.assertEqual(context["is_active"], True)

        plugin_instance = plugin2.get_plugin_class_instance()
        context = plugin_instance.render({}, plugin2, None)

        self.assertIn("is_active", context)
        self.assertEqual(context["is_active"], False)

    def test_first_carousel_content_active_render(self):
        target = add_plugin(
            placeholder=self.placeholder,
            plugin_type="CarouselPlugin",
            language=self.language,
        )
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="CarouselContentPlugin",
            language=self.language,
            target=target,
        )

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = "<div class='carousel-item active'></div>"

        self.assertHTMLEqual(html, expected_html)

    def test_carousel_content_plugin_caption(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type="CarouselContentPlugin",
            language=self.language,
            caption_html="""<h2>Title</h2><p>Lorem ipsum</p>"""
        )
        plugin.full_clean()
        
        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(plugin, {})
        expected_html = """
        <div class="carousel-item active">
            <div class="carousel-caption d-none d-md-block">
                <h2>Title</h2><p>Lorem ipsum</p>
            </div>
        </div>
        """

        self.assertHTMLEqual(html, expected_html)

    def test_carousel_plugin_indicators_render_html(self):
        target = add_plugin(
            placeholder=self.placeholder,
            plugin_type="CarouselPlugin",
            language=self.language,
            enable_indicators=True,
        )
        add_plugin(
            placeholder=self.placeholder,
            plugin_type="CarouselContentPlugin",
            language=self.language,
            target=target,
        )
        add_plugin(
            placeholder=self.placeholder,
            plugin_type="CarouselContentPlugin",
            language=self.language,
            target=target,
        )

        renderer = ContentRenderer(request=RequestFactory())

        html = renderer.render_plugin(target, {})
        expected_html = f"""
        <div class="carousel-indicators">
            <button type="button" data-bs-target="#carousel-{target.id}" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 0"></button>
            <button type="button" data-bs-target="#carousel-{target.id}" data-bs-slide-to="1" aria-current="true" aria-label="Slide 1"></button>
        </div>
        """

        self.assertInHTML(expected_html, html)