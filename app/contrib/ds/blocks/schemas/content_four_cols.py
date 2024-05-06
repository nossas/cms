from contrib.ds.blocks.models import BlockLayout, FlexDirection, AlignmentItems
from contrib.ds.link.models import Context

name = "Conteúdo 4 colunas"

schema = {
    "children": [
        {
            "plugin_type": "TextPlugin",
            "attrs": {
                "body": f"<p style='text-align:center'>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent pretium quam porta porta pellentesque. Duis hendrerit risus at massa commodo ultrices. Donec a purus egestas, tristique nunc sed, consequat ipsum.</p>"
            },
        },        
        {
            "plugin_type": "BlockPlugin",
            "attrs": {
                "layout": BlockLayout.grid,
                "attributes": {"gap": 2}
            },
            "children": [
                {
                    "plugin_type": "ColumnPlugin",
                    "attrs": {
                        "span": 3,
                        "span_mobile": 12
                    },
                    "children": [
                        {
                            "plugin_type": "PicturePlugin",
                            "attrs": {
                                "external_picture": "https://place-hold.it/120x120",
                                "alignment": " mx-auto"
                            }
                        },
                        {
                            "plugin_type": "TextPlugin",
                            "attrs": {
                                "body": f"<h2 style='text-align:center'>Lorem ipsum {i}</h2>"
                            },
                        },
                    ]
                } for i in range(4)
            ]
        }
    ],
}