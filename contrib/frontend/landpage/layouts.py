from django.conf import settings

from cms.api import add_plugin
from filer.models import Image

from contrib.frontend.grid.models import (
    XAlignmentChoices,
    YAlignmentChoices,
    GridColumnChoices,
)
from contrib.frontend.models import SocialMediaItem, SocialMediaChoices, PartnersItem, PartnersColumnChoices

from .models import Block, AlignmentChoices
from .forms import LayoutChoices


class Layout(object):
    def __init__(self, obj: Block, layout: any):
        """Copy plugins to a placeholder based on layout.
        Args:
            obj (Block): Block object.
            layout (LayoutChoices): Layout choice."""

        self.obj = obj
        self.layout = layout

    def copy(self):
        getattr(self, f"_{self.layout}_copy")(self.obj, self.layout)

    def _hero_copy(self, obj: Block, layout: any):
        self.__make_hero(obj, layout)

    def _hero_nobrand_copy(self, obj: Block, layout: any):
        self.__make_hero(obj, layout)

    def __make_hero(self, obj: Block, layout: any):
        # Configurar o alinhamento do bloco ao centro
        obj.alignment = AlignmentChoices.center
        obj.save()

        if layout == LayoutChoices.hero_nobrand:
            add_plugin(
                placeholder=obj.placeholder,
                plugin_type="TextPlugin",
                language=obj.language,
                target=obj,
                body='<h2 class="text-center">Título do bloco</h2>',
            )
        else:
            add_plugin(
                placeholder=obj.placeholder,
                plugin_type="PicturePlugin",
                language=obj.language,
                target=obj,
                external_picture=settings.STATIC_URL
                + "images/examples/Hero - Logo da campanha.png",
            )

        add_plugin(
            placeholder=obj.placeholder,
            plugin_type="TextPlugin",
            language=obj.language,
            target=obj,
            body="<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.</p>",
        )
        add_plugin(
            placeholder=obj.placeholder,
            plugin_type="ButtonPlugin",
            language=obj.language,
            target=obj,
            title="Pressione",
            action_url="#",
        )

    def _four_columns_copy(self, obj: Block, layout: any):
        self._tree_columns_copy(obj, layout)

    def _tree_columns_copy(self, obj: Block, layout: any):
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
            cols=GridColumnChoices.grid_4
            if layout == LayoutChoices.four_columns
            else GridColumnChoices.grid_3,
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
                external_picture=settings.STATIC_URL + "images/examples/Coluna.png",
            )

            add_plugin(
                placeholder=col_obj.placeholder,
                plugin_type="TextPlugin",
                language=col_obj.language,
                target=col_obj,
                body="<p style='text-align:center;'>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.</p>",
            )

    def _two_columns_b_copy(self, obj: Block, layout: any):
        self._two_columns_a_copy(obj, layout)

    def _two_columns_a_copy(self, obj: Block, layout: any):
        grid_obj = add_plugin(
            placeholder=obj.placeholder,
            plugin_type="GridPlugin",
            language=obj.language,
            target=obj,
            cols=GridColumnChoices.grid_2
            if layout == LayoutChoices.two_columns_a
            else GridColumnChoices.grid_1_2,
        )
        # Coluna da Esquerda
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
            external_picture=settings.STATIC_URL + "images/examples/6x6.png"
            if layout == LayoutChoices.two_columns_a
            else settings.STATIC_URL + "images/examples/4x8.png",
        )
        # Coluna da Direita
        col_obj = add_plugin(
            placeholder=grid_obj.placeholder,
            plugin_type="ColumnPlugin",
            language=grid_obj.language,
            target=grid_obj,
            alignment_x=XAlignmentChoices.start,
            alignment_y=YAlignmentChoices.center,
        )
        add_plugin(
            placeholder=col_obj.placeholder,
            plugin_type="TextPlugin",
            language=col_obj.language,
            target=col_obj,
            body="<h2>Título do bloco</h2>",
        )
        text = """
            <div>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.</p>
            <br/>
            <a href="#" target="self">Link</a>
            </div>
            """
        add_plugin(
            placeholder=col_obj.placeholder,
            plugin_type="TextPlugin",
            language=col_obj.language,
            target=col_obj,
            body=text,
        )

    def _signature_copy(self, obj: Block, layout: any):
        grid_obj = add_plugin(
            placeholder=obj.placeholder,
            plugin_type="GridPlugin",
            language=obj.language,
            target=obj,
            cols=GridColumnChoices.grid_1_2,
        )
        # Coluna da esquerda
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
            external_picture=settings.STATIC_URL + "images/examples/Assinatura.png",
        )
        # Coluna da direita
        col_obj = add_plugin(
            placeholder=grid_obj.placeholder,
            plugin_type="ColumnPlugin",
            language=grid_obj.language,
            target=grid_obj,
            alignmnet_x=XAlignmentChoices.start,
            alignment_y=YAlignmentChoices.center
        )
        
        add_plugin(
            placeholder=col_obj.placeholder,
            plugin_type="TextPlugin",
            language=col_obj.language,
            target=col_obj,
            body="""
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.</p>
            """
        )   

        socialmedia_plugin = add_plugin(
            placeholder=col_obj.placeholder,
            plugin_type="SocialMediaPlugin",
            language=col_obj.language,
            target=col_obj,
        )
        
        for choice in [SocialMediaChoices.facebook, SocialMediaChoices.instagram]:
            SocialMediaItem.objects.create(
                kind=choice,
                external_icon=settings.STATIC_URL + f"images/examples/Social Media {choice.capitalize()}.png",
                plugin=socialmedia_plugin
            )

    def _signature_partners_a_copy(self, obj: Block, layout: any):
        grid_obj = add_plugin(
            placeholder=obj.placeholder,
            plugin_type="GridPlugin",
            language=obj.language,
            target=obj,
            cols=GridColumnChoices.grid_1_2,
        )

        # Coluna da esquerda
        col_obj = add_plugin(
            placeholder=grid_obj.placeholder,
            plugin_type="ColumnPlugin",
            language=grid_obj.language,
            target=grid_obj,
        )
        add_plugin(
            placeholder=col_obj.placeholder,
            plugin_type="TextPlugin",
            language=col_obj.language,
            target=col_obj,
            body="<h1>Quem assina</h1>",
        )
        add_plugin(
            placeholder=col_obj.placeholder,
            plugin_type="PicturePlugin",
            language=col_obj.language,
            target=col_obj,
            external_picture=settings.STATIC_URL + "images/examples/Assinatura Logo.png",
        )
        add_plugin(
            placeholder=col_obj.placeholder,
            plugin_type="TextPlugin",
            language=col_obj.language,
            target=col_obj,
            body="<p style='text-align:center;'>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.</p>",
        )

        # Coluna da direita
        col_obj = add_plugin(
            placeholder=grid_obj.placeholder,
            plugin_type="ColumnPlugin",
            language=grid_obj.language,
            target=grid_obj,
            alignment_y=YAlignmentChoices.center
        )
        partners_obj = add_plugin(
            placeholder=col_obj.placeholder,
            plugin_type="PartnersPlugin",
            language=col_obj.language,
            target=col_obj,
            cols=PartnersColumnChoices.cols_4
        )

        for _ in range(8):
            PartnersItem.objects.create(
                external_picture=settings.STATIC_URL + "images/examples/Logo Parceiro.png",
                plugin=partners_obj
            )


    def _signature_partners_b_copy(self, obj: Block, layout: any):
        obj.alignment = AlignmentChoices.center
        obj.save()
        
        add_plugin(
            placeholder=obj.placeholder,
            plugin_type="TextPlugin",
            language=obj.language,
            target=obj,
            body="<h1>Quem Assina</h1>",
        )
        partners_obj = add_plugin(
            placeholder=obj.placeholder,
            plugin_type="PartnersPlugin",
            language=obj.language,
            target=obj,
            cols=PartnersColumnChoices.cols_6
        )

        for _ in range(12):
            PartnersItem.objects.create(
                external_picture=settings.STATIC_URL + "images/examples/Logo Parceiro.png",
                plugin=partners_obj
            )
