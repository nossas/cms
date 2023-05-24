# Generated by Django 3.2 on 2023-05-18 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        ('mob', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='mob_block', serialize=False, to='cms.cmsplugin')),
                ('title', models.CharField(blank=True, max_length=80, verbose_name='título')),
                ('slug', models.SlugField(blank=True, help_text='a parte do título que é usada na URL', max_length=80, verbose_name='slug')),
                ('menu_title', models.CharField(blank=True, max_length=50, verbose_name='título do menu')),
                ('menu_hidden', models.BooleanField(default=False, verbose_name='esconder menu?')),
                ('background', models.CharField(blank=True, default='white', max_length=200, verbose_name='background')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.DeleteModel(
            name='HeroPlugin',
        ),
    ]