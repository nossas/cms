# Generated by Django 3.2 on 2023-06-14 20:39

import colorfield.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='Button',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='frontend_button', serialize=False, to='cms.cmsplugin')),
                ('font', models.CharField(blank=True, choices=[('Abel', 'Abel'), ('Anton', 'Anton'), ('Archivo Narrow', 'Archivo Narrow'), ('Arvo', 'Arvo'), ('Asap', 'Asap'), ('Baloo Bhai', 'Baloo Bhai'), ('Bitter', 'Bitter'), ('Bree Serif', 'Bree Serif'), ('Cabin', 'Cabin'), ('Catamaran', 'Catamaran'), ('Crimson Text', 'Crimson Text'), ('Cuprum', 'Cuprum'), ('David Libre', 'David Libre'), ('Dosis', 'Dosis'), ('Droid Sans', 'Droid Sans'), ('Exo', 'Exo'), ('Exo 2', 'Exo 2'), ('Fira Sans', 'Fira Sans'), ('Fjalla One', 'Fjalla One'), ('Francois One', 'Francois One'), ('Gidugu', 'Gidugu'), ('Hind', 'Hind'), ('Inconsolata', 'Inconsolata'), ('Indie Flower', 'Indie Flower'), ('Josefin Sans', 'Josefin Sans'), ('Karla', 'Karla'), ('Lalezar', 'Lalezar'), ('Lato', 'Lato'), ('Libre Baskerville', 'Libre Baskerville'), ('Lobster', 'Lobster'), ('Lora', 'Lora'), ('Merriweather Sans', 'Merriweather Sans'), ('Montserrat', 'Montserrat'), ('Muli', 'Muli'), ('Noto Serif', 'Noto Serif'), ('Nunito Sans', 'Nunito Sans'), ('Open Sans', 'Open Sans'), ('Open Sans Condensed', 'Open Sans Condensed'), ('Oswald', 'Oswald'), ('Oxygen', 'Oxygen'), ('PT Sans', 'PT Sans'), ('PT Serif', 'PT Serif'), ('Pacifico', 'Pacifico'), ('Playfair Display', 'Playfair Display'), ('Poiret One', 'Poiret One'), ('Poppins', 'Poppins'), ('Quicksand', 'Quicksand'), ('Raleway', 'Raleway'), ('Roboto', 'Roboto'), ('Roboto Condensed', 'Roboto Condensed'), ('Roboto Mono', 'Roboto Mono'), ('Roboto Slab', 'Roboto Slab'), ('Ruslan Display', 'Ruslan Display'), ('Signika', 'Signika'), ('Slabo 27px', 'Slabo 27px'), ('Source Sans Pro', 'Source Sans Pro'), ('Titillium Web', 'Titillium Web'), ('Ubuntu', 'Ubuntu'), ('Ubuntu Condensed', 'Ubuntu Condensed'), ('Varela Round', 'Varela Round'), ('Yanone Kaffeesatz', 'Yanone Kaffeesatz')], max_length=100, null=True, verbose_name='Estilo de fonte')),
                ('color', colorfield.fields.ColorField(blank=True, default=None, image_field=None, max_length=18, null=True, samples=[('#FFFFFF', 'white'), ('#000000', 'black')], verbose_name='Cor da fonte')),
                ('background_color', colorfield.fields.ColorField(blank=True, default=None, image_field=None, max_length=18, null=True, samples=[('#FFFFFF', 'white'), ('#000000', 'black')], verbose_name='Cor de fundo')),
                ('title', models.CharField(max_length=80, verbose_name='Título')),
                ('action_url', models.CharField(help_text='slug do bloco usado na URL', max_length=200, verbose_name='endereço da ação')),
                ('target_blank', models.BooleanField(default=False, verbose_name='Abrir em nova aba?')),
                ('bold', models.BooleanField(default=False, verbose_name='Negrito?')),
                ('border_color', colorfield.fields.ColorField(blank=True, default=None, image_field=None, max_length=18, null=True, samples=[('#FFFFFF', 'white'), ('#000000', 'black')], verbose_name='Cor da borda')),
                ('border_size', models.CharField(blank=True, choices=[('border', 'Padrão (1px)'), ('border-0', 'Sem borda (0px)'), ('border-2', 'Pequeno (2px)'), ('border-4', 'Médio (4px)'), ('border-8', 'Grande (8px)')], max_length=30, null=True, verbose_name='Tamanho da borda')),
                ('rounded', models.CharField(blank=True, choices=[('rounded-none', 'Sem arredondamento'), ('rounded-sm', 'Small'), ('rounded-md', 'Medium'), ('rounded-lg', 'Large'), ('rounded-xl', 'Extra Large')], max_length=30, null=True, verbose_name='Arredondamento')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin', models.Model),
        ),
    ]
