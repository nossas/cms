import math
from typing import Tuple
from django.conf import settings

from cms.api import add_plugin
from filer.models import Image

from contrib.frontend.grid.models import (
    XAlignmentChoices,
    YAlignmentChoices,
    GridColumnChoices,
    ColumnSpacingChoices,
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

    def is_dark(self):
        if self.obj.background_color:
            hexColor = self.obj.background_color.lstrip("#")

            [r, g, b] = tuple(int(hexColor[i : i + 2], 16) for i in (0, 2, 4))

            hsp = math.sqrt(0.299 * (r * r) + 0.587 * (g * g) + 0.114 * (b * b))

            if hsp > 157.5:
                return False

            return True
    
    def color_apply(self, paragraph: str, color: str = "white", element: str = "p") -> str:
        lines = []

        for text in paragraph.split(f"</{element}>"):
            try:
                init_p, inner_html = text.split(">", 1)
                lines.extend([init_p, '>', f'<span style="color:{color};">', inner_html, f'</span></{element}>'])
            except ValueError:
                lines.append(text)
        
        return "".join(lines)

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
        body_html = """
        <p>Narrativa lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat</p>
        <p><br>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
        <p><br>Narrativa lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
        <p><br>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
        """
        add_plugin(
            placeholder=col_obj.placeholder,
            plugin_type="TextPlugin",
            language=self.obj.language,
            target=col_obj,
            # Attributos de Pressure,
            body=self.color_apply(body_html) if self.is_dark() else body_html,
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
            text_html = '<h1 class="text-center">Título do bloco</h1>'
            add_plugin(
                placeholder=self.obj.placeholder,
                plugin_type="TextPlugin",
                language=self.obj.language,
                target=self.obj,
                body=self.color_apply(text_html, element="h1") if self.is_dark() else text_html
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
            body=self.color_apply(paragraph) if self.is_dark() else paragraph,
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

        text_html = '<h2 class="text-center">Título do bloco</h2>'
        add_plugin(
            placeholder=self.obj.placeholder,
            plugin_type="TextPlugin",
            language=self.obj.language,
            target=self.obj,
            body=self.color_apply(text_html, element="h2") if self.is_dark() else text_html
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

            paragraph = "<p style='text-align:center;'>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.</p>"
            add_plugin(
                placeholder=col_obj.placeholder,
                plugin_type="TextPlugin",
                language=col_obj.language,
                target=col_obj,
                body=self.color_apply(paragraph) if self.is_dark() else paragraph,
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

        text_html = "<h2>Título do bloco</h2>"
        add_plugin(
            placeholder=col_obj.placeholder,
            plugin_type="TextPlugin",
            language=col_obj.language,
            target=col_obj,
            body=self.color_apply(text_html, element="h2") if self.is_dark() else text_html
        )
        
        p = "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.</p>"
        text = """
            <div>
            """
        text += self.color_apply(p) if self.is_dark() else p
        text += """
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

        text_html = "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.</p>"
        add_plugin(
            placeholder=col_obj.placeholder,
            plugin_type="TextPlugin",
            language=col_obj.language,
            target=col_obj,
            body=self.color_apply(text_html) if self.is_dark() else text_html,
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
        col_obj.save()

        text_html = "<h2>Quem assina</h2>"
        add_plugin(
            placeholder=col_obj.placeholder,
            plugin_type="TextPlugin",
            language=col_obj.language,
            target=col_obj,
            body=self.color_apply(text_html, element="h2") if self.is_dark() else text_html
        )
        add_plugin(
            placeholder=col_obj.placeholder,
            plugin_type="PicturePlugin",
            language=col_obj.language,
            target=col_obj,
            external_picture=settings.STATIC_URL
            + "images/examples/Assinatura Logo.png",
        )

        text_html = "<p style='text-align:center;'>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.</p>"
        add_plugin(
            placeholder=col_obj.placeholder,
            plugin_type="TextPlugin",
            language=col_obj.language,
            target=col_obj,
            body=self.color_apply(text_html) if self.is_dark() else text_html,
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

        text_html = "<h2>Quem Assina</h2>"
        add_plugin(
            placeholder=self.obj.placeholder,
            plugin_type="TextPlugin",
            language=self.obj.language,
            target=self.obj,
            body=self.color_apply(text_html, element="h2") if self.is_dark() else text_html
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
