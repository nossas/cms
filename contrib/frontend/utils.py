from django.conf import settings

from cms.api import add_plugin

from .models import LayoutChoices, ColumnChoices


def copy_by_layout(obj, layout):
    if layout == LayoutChoices.tree_columns or layout == LayoutChoices.four_columns:
        add_plugin(
            placeholder=obj.placeholder,
            plugin_type="TextPlugin",
            language=obj.language,
            target=obj,
            body='<h2 class="text-center">Título do bloco</h2>',
        )

        grid_obj = add_plugin(
            placeholder=obj.placeholder,
            plugin_type="GridPlugin",
            language=obj.language,
            target=obj,
            cols=ColumnChoices.grid_4
            if layout == LayoutChoices.four_columns
            else ColumnChoices.grid_3,
        )

        for x in range(4 if layout == LayoutChoices.four_columns else 3):
            col_obj = add_plugin(
                placeholder=grid_obj.placeholder,
                plugin_type="ColumnPlugin",
                language=grid_obj.language,
                target=grid_obj,
            )

            add_plugin(
                placeholder=col_obj.placeholder,
                plugin_type="PicturePlugin",
                language=col_obj.language,
                target=col_obj,
                external_picture=settings.STATIC_URL + "images/img.png",
            )

            add_plugin(
                placeholder=col_obj.placeholder,
                plugin_type="TextPlugin",
                language=col_obj.language,
                target=col_obj,
                body="<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.</p>",
            )
