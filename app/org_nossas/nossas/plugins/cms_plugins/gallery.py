from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool


@plugin_pool.register_plugin
class GalleryPlugin(CMSPluginBase):
    name = "Galeria"
    module = "NOSSAS"
    render_template = "nossas/plugins/gallery.html"
    child_classes = [
        "PicturePlugin"
    ]
    allow_children = True