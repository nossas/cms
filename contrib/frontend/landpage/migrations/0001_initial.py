# Generated by Django 3.2 on 2023-06-13 15:46

import colorfield.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Navbar',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='landpage_navbar', serialize=False, to='cms.cmsplugin')),
                ('font', models.CharField(blank=True, choices=[('Abel', 'Abel'), ('Anton', 'Anton'), ('Archivo Narrow', 'Archivo Narrow'), ('Arvo', 'Arvo'), ('Asap', 'Asap'), ('Baloo Bhai', 'Baloo Bhai'), ('Bitter', 'Bitter'), ('Bree Serif', 'Bree Serif'), ('Cabin', 'Cabin'), ('Catamaran', 'Catamaran'), ('Crimson Text', 'Crimson Text'), ('Cuprum', 'Cuprum'), ('David Libre', 'David Libre'), ('Dosis', 'Dosis'), ('Droid Sans', 'Droid Sans'), ('Exo', 'Exo'), ('Exo 2', 'Exo 2'), ('Fira Sans', 'Fira Sans'), ('Fjalla One', 'Fjalla One'), ('Francois One', 'Francois One'), ('Gidugu', 'Gidugu'), ('Hind', 'Hind'), ('Inconsolata', 'Inconsolata'), ('Indie Flower', 'Indie Flower'), ('Josefin Sans', 'Josefin Sans'), ('Karla', 'Karla'), ('Lalezar', 'Lalezar'), ('Lato', 'Lato'), ('Libre Baskerville', 'Libre Baskerville'), ('Lobster', 'Lobster'), ('Lora', 'Lora'), ('Merriweather Sans', 'Merriweather Sans'), ('Montserrat', 'Montserrat'), ('Muli', 'Muli'), ('Noto Serif', 'Noto Serif'), ('Nunito Sans', 'Nunito Sans'), ('Open Sans', 'Open Sans'), ('Open Sans Condensed', 'Open Sans Condensed'), ('Oswald', 'Oswald'), ('Oxygen', 'Oxygen'), ('PT Sans', 'PT Sans'), ('PT Serif', 'PT Serif'), ('Pacifico', 'Pacifico'), ('Playfair Display', 'Playfair Display'), ('Poiret One', 'Poiret One'), ('Poppins', 'Poppins'), ('Quicksand', 'Quicksand'), ('Raleway', 'Raleway'), ('Roboto', 'Roboto'), ('Roboto Condensed', 'Roboto Condensed'), ('Roboto Mono', 'Roboto Mono'), ('Roboto Slab', 'Roboto Slab'), ('Ruslan Display', 'Ruslan Display'), ('Signika', 'Signika'), ('Slabo 27px', 'Slabo 27px'), ('Source Sans Pro', 'Source Sans Pro'), ('Titillium Web', 'Titillium Web'), ('Ubuntu', 'Ubuntu'), ('Ubuntu Condensed', 'Ubuntu Condensed'), ('Varela Round', 'Varela Round'), ('Yanone Kaffeesatz', 'Yanone Kaffeesatz')], max_length=100, null=True, verbose_name='Estilo de fonte')),
                ('color', colorfield.fields.ColorField(blank=True, default=None, image_field=None, max_length=18, null=True, samples=[('#FFFFFF', 'white'), ('#000000', 'black')], verbose_name='Cor da fonte')),
                ('background_color', colorfield.fields.ColorField(blank=True, default=None, image_field=None, max_length=18, null=True, samples=[('#FFFFFF', 'white'), ('#000000', 'black')], verbose_name='Cor de fundo')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin', models.Model),
        ),
        migrations.CreateModel(
            name='Block',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='landpage_block', serialize=False, to='cms.cmsplugin')),
                ('title', models.CharField(blank=True, max_length=80, verbose_name='título')),
                ('slug', models.SlugField(blank=True, help_text='a parte do título que é usada na URL', max_length=80, verbose_name='slug')),
                ('menu_title', models.CharField(blank=True, help_text='padrão é igual ao título do bloco', max_length=50, verbose_name='título do menu')),
                ('menu_hidden', models.BooleanField(default=False, verbose_name='esconder menu?')),
                ('hidden', models.BooleanField(default=False, verbose_name='esconder bloco?')),
                ('spacing', models.CharField(choices=[('py-8', 'Extra small'), ('py-10', 'Small'), ('py-12', 'Default'), ('py-14', 'Large'), ('py-16', 'Extra large')], default='py-12', max_length=30, verbose_name='espaçamento')),
                ('alignment', models.CharField(blank=True, choices=[('grid justify-items-center', 'Centralizar'), ('grid justify-items-start', 'Esquerda'), ('grid justify-items-end', 'Direita')], default='grid justify-items-start', max_length=30, null=True, verbose_name='alinhamento')),
                ('background_color', colorfield.fields.ColorField(blank=True, default=None, image_field=None, max_length=18, null=True, samples=[('#FFFFFF', 'white'), ('#000000', 'black')])),
                ('background_image', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.FILER_IMAGE_MODEL, verbose_name='Imagem de fundo')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin', models.Model),
        ),
    ]