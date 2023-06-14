from typing import Tuple
from django.conf import settings

from cms.api import add_plugin
from filer.models import Image

from contrib.frontend.grid.models import (
    XAlignmentChoices,
    YAlignmentChoices,
    GridColumnChoices,
    ColumnSpacingChoices
)
from contrib.frontend.models import (
    SocialMediaItem,
    SocialMediaChoices,
    PartnersItem,
    PartnersColumnChoices,
)

from .models import Block, AlignmentChoices, SpacingChoices
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
        if self.layout:
            getattr(self, f"_{self.layout}_copy")()

    def create_grid(self, n_cols: str) -> Tuple:
        """
        Criar grid e colunas a partir do número de colunas definidos
        Args:
            n_cols (str): 1 | 2 | 3 | 4 | 1_2
        """
        if "_" not in n_cols:
            n = int(n_cols)
        else:
            # TODO: Melhorar essa lógica de escolha
            n = int(n_cols.split("_")[1])

        grid = add_plugin(
            placeholder=self.obj.placeholder,
            plugin_type="GridPlugin",
            language=self.obj.language,
            target=self.obj,
            cols=getattr(GridColumnChoices, f"grid_{n_cols}"),
        )

        cols = []
        for x in range(n):
            cols.append(
                add_plugin(
                    placeholder=grid.placeholder,
                    plugin_type="ColumnPlugin",
                    language=grid.language,
                    target=grid,
                )
            )

        return grid, cols

    def _pressure_copy(self):
        self.obj.spacing = SpacingChoices.py_small
        self.obj.save()
        # Adiciona plugin de grid
        grid, cols = self.create_grid(n_cols="2")

        # Coluna da esquerda
        col_obj = cols[0]
        add_plugin(
            placeholder=col_obj.placeholder,
            plugin_type="PressurePlugin",
            language=self.obj.language,
            target=col_obj,
            # Attributos de Pressure,
            email_subject='["Sou contra o aumento abusivo do trem!"]',
            email_body="""
Prezado,
Entra ano e sai ano, e mais uma vez estou aqui pedindo para que o aumento do valor da passagem seja suspenso. Parece que todos os anos precisamos vir aqui nos mobilizar para que as propostas de aumento completamente absurdas sejam suspensas. Nós, usuários da supervia viemos vir aqui nos mobilizar para que as propostas de...
            """,
        )

        col_obj = cols[1]
        add_plugin(
            placeholder=col_obj.placeholder,
            plugin_type="TextPlugin",
            language=self.obj.language,
            target=col_obj,
            # Attributos de Pressure,
            body="""
            <p>Narrativa lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat</p>
            <p><br>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
            <p><br>Narrativa lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
            <p><br>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
            """,
        )

    def _hero_copy(self):
        self.__make_hero()

    def _hero_nobrand_copy(self):
        self.__make_hero()

    def __make_hero(self):
        # Configurar o alinhamento do bloco ao centro
        self.obj.spacing = SpacingChoices.py_extra_large
        self.obj.alignment = AlignmentChoices.center
        self.obj.save()

        if self.layout == LayoutChoices.hero_nobrand:
            add_plugin(
                placeholder=self.obj.placeholder,
                plugin_type="TextPlugin",
                language=self.obj.language,
                target=self.obj,
                body='<h2 class="text-center">Título do bloco</h2>',
            )
        else:
            add_plugin(
                placeholder=self.obj.placeholder,
                plugin_type="PicturePlugin",
                language=self.obj.language,
                target=self.obj,
                external_picture=settings.STATIC_URL
                + "images/examples/Hero - Logo da campanha.png",
            )

        paragraph = """
        <p style="text-align:center;">
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor<br/>
        incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud<br/>
        exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
        </p>
        """
        add_plugin(
            placeholder=self.obj.placeholder,
            plugin_type="TextPlugin",
            language=self.obj.language,
            target=self.obj,
            body=paragraph,
        )
        add_plugin(
            placeholder=self.obj.placeholder,
            plugin_type="ButtonPlugin",
            language=self.obj.language,
            target=self.obj,
            title="Pressione",
            action_url="#",
        )

    def _four_columns_copy(self):
        self._tree_columns_copy()

    def _tree_columns_copy(self):
        self.obj.alignment = AlignmentChoices.center
        self.obj.save()

        add_plugin(
            placeholder=self.obj.placeholder,
            plugin_type="TextPlugin",
            language=self.obj.language,
            target=self.obj,
            body='<h2 class="text-center">Título do bloco</h2>',
        )

        grid, cols = self.create_grid(
            n_cols="4" if self.layout == LayoutChoices.four_columns else "3"
        )

        for col_obj in cols:
            col_obj.spacing = ColumnSpacingChoices.gap_8
            col_obj.save()

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

    def _two_columns_b_copy(self):
        self._two_columns_a_copy()

    def _two_columns_a_copy(self):
        grid, cols = self.create_grid(
            n_cols="2" if self.layout == LayoutChoices.two_columns_a else "1_2"
        )

        # Coluna da Esquerda
        col_obj = cols[0]
        add_plugin(
            placeholder=col_obj.placeholder,
            plugin_type="PicturePlugin",
            language=col_obj.language,
            target=col_obj,
            external_picture=settings.STATIC_URL + "images/examples/6x6.png"
            if self.layout == LayoutChoices.two_columns_a
            else settings.STATIC_URL + "images/examples/4x8.png",
        )
        # Coluna da Direita
        col_obj = cols[1]
        col_obj.spacing = ColumnSpacingChoices.gap_8
        col_obj.alignment_x = XAlignmentChoices.start
        col_obj.alignment_y = YAlignmentChoices.center
        col_obj.save()

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

    def _signature_copy(self):
        self.obj.spacing = SpacingChoices.py_large
        self.obj.menu_hidden = True
        self.obj.save()

        grid, cols = self.create_grid(n_cols="1_2")

        # Coluna da esquerda
        col_obj = cols[0]
        col_obj.alignment_x = XAlignmentChoices.right
        col_obj.save()

        add_plugin(
            placeholder=col_obj.placeholder,
            plugin_type="PicturePlugin",
            language=col_obj.language,
            target=col_obj,
            external_picture=settings.STATIC_URL + "images/examples/Assinatura.png",
        )
        # Coluna da direita
        col_obj = cols[1]
        col_obj.spacing = ColumnSpacingChoices.gap_8
        col_obj.alignment_x = XAlignmentChoices.start
        col_obj.alignment_y = YAlignmentChoices.center
        col_obj.save()

        add_plugin(
            placeholder=col_obj.placeholder,
            plugin_type="TextPlugin",
            language=col_obj.language,
            target=col_obj,
            body="""
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.</p>
            """,
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
                external_picture=settings.STATIC_URL
                + f"images/examples/Social Media {choice.capitalize()}.png",
                plugin=socialmedia_plugin,
            )

    def _signature_partners_a_copy(self):
        self.obj.spacing = SpacingChoices.py_large
        self.obj.save()

        grid, cols = self.create_grid(n_cols="1_2")

        # Coluna da esquerda
        col_obj = cols[0]
        col_obj.spacing = ColumnSpacingChoices.gap_8
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
            external_picture=settings.STATIC_URL
            + "images/examples/Assinatura Logo.png",
        )
        add_plugin(
            placeholder=col_obj.placeholder,
            plugin_type="TextPlugin",
            language=col_obj.language,
            target=col_obj,
            body="<p style='text-align:center;'>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.</p>",
        )

        # Coluna da direita
        col_obj = cols[1]
        col_obj.alignment_y = YAlignmentChoices.center
        col_obj.save()

        partners_obj = add_plugin(
            placeholder=col_obj.placeholder,
            plugin_type="PartnersPlugin",
            language=col_obj.language,
            target=col_obj,
            cols=PartnersColumnChoices.cols_4,
        )

        for _ in range(8):
            PartnersItem.objects.create(
                external_picture=settings.STATIC_URL
                + "images/examples/Logo Parceiro.png",
                plugin=partners_obj,
            )

    def _signature_partners_b_copy(self):
        self.obj.alignment = AlignmentChoices.center
        self.obj.save()

        add_plugin(
            placeholder=self.obj.placeholder,
            plugin_type="TextPlugin",
            language=self.obj.language,
            target=self.obj,
            body="<h1>Quem Assina</h1>",
        )
        partners_obj = add_plugin(
            placeholder=self.obj.placeholder,
            plugin_type="PartnersPlugin",
            language=self.obj.language,
            target=self.obj,
            cols=PartnersColumnChoices.cols_6,
        )

        for _ in range(12):
            PartnersItem.objects.create(
                external_picture=settings.STATIC_URL
                + "images/examples/Logo Parceiro.png",
                plugin=partners_obj,
            )
