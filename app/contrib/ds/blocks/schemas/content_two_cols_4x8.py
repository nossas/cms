from contrib.ds.blocks.models import BlockLayout, FlexDirection, AlignmentItems
from contrib.ds.link.models import Context

name = "Conteúdo 2 colunas (4x6)"

schema = {
    "attrs": {"layout": BlockLayout.grid, "attributes": {"gap": 2}},
    "children": [
        {
            "plugin_type": "ColumnPlugin",
            "attrs": {"span": 4, "span_mobile": 12},
            "children": [
                {
                    "plugin_type": "PicturePlugin",
                    "attrs": {
                        "attributes": {"class": "img-fluid"},
                        "external_picture": "https://place-hold.it/500x300",
                    },
                },
            ],
        },
        {
            "plugin_type": "ColumnPlugin",
            "attrs": {"span": 8, "span_mobile": 12},
            "children": [
                {
                    "plugin_type": "TextPlugin",
                    "attrs": {
                        "body": f"<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent pretium quam porta porta pellentesque. Duis hendrerit risus at massa commodo ultrices. Donec a purus egestas, tristique nunc sed, consequat ipsum.</p>"
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
        },
    ],
}
