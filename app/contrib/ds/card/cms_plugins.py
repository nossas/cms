from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import Card


@plugin_pool.register_plugin
class CardPlugin(CMSPluginBase):
    name = "Cartão"
    model = Card
    render_template = "card/plugins/card.html"
    allow_children = True
    child_classes = ["TextPlugin", "ButtonPlugin"]