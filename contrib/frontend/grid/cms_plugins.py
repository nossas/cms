# Grid
# Coluna
from cms.plugin_pool import plugin_pool, CMSPluginBase

from .models import Grid, Column


@plugin_pool.register_plugin
class GridPlugin(CMSPluginBase):
    name = "Grid"
    module = "Frontend"
    model = Grid
    render_template = "frontend/grid/plugins/grid.html"
    allow_children = True
    child_classes = [
        "ColumnPlugin",
    ]


@plugin_pool.register_plugin
class ColumnPlugin(CMSPluginBase):
    name = "Coluna"
    module = "Frontend"
    model = Column
    render_template = "frontend/grid/plugins/column.html"
    allow_children = True
    child_classes = [
        "PicturePlugin",
        "TextPlugin",
        "ButtonPlugin",
        "SocialMediaPlugin",
        "PartnersPlugin",
        "PressurePlugin"
    ]