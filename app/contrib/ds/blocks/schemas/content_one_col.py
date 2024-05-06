from contrib.ds.blocks.models import BlockLayout, FlexDirection, AlignmentItems
from contrib.ds.link.models import Context

name = "Conteúdo 1 coluna"

schema = {
    "attrs": {
        "layout": BlockLayout.flex,
        "attributes": {
            "alignment": AlignmentItems.center,
            "direction": FlexDirection.column,
        },
    },
    "children": [
        {
            "plugin_type": "TextPlugin",
            "attrs": {
                "body": "<h2 style='text-align:center'>Lorem ipsum</h2><p style='text-align:center'>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent pretium quam porta porta pellentesque. Duis hendrerit risus at massa commodo ultrices. Donec a purus egestas, tristique nunc sed, consequat ipsum.</p>"
            },
        },
        {
            "plugin_type": "ButtonPlugin",
            "attrs": {
                "label": "Ação",
                "external_link": "http://nossas.org",
                "context": Context.primary,
            },
        },
    ],
}