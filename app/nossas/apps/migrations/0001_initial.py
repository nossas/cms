# Generated by Django 3.2 on 2024-01-26 15:20

import cms.models.fields
from django.conf import settings
import django.contrib.sites.managers
from django.db import migrations, models
import django.db.models.deletion
import filer.fields.image
import tag_fields.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ('sites', '0002_alter_domain_unique'),
        ('tag_fields', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampaignListPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='apps_campaignlistpluginmodel', serialize=False, to='cms.cmsplugin')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='CampaignGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=180, verbose_name='Nome da grupo')),
                ('community_id', models.IntegerField(verbose_name='ID da Comunidade BONDE')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.site')),
            ],
            options={
                'verbose_name': 'Comunidade',
                'unique_together': {('site', 'community_id')},
            },
            managers=[
                ('on_site', django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=180, verbose_name='Nome da campanha')),
                ('description_pt_br', models.TextField(verbose_name='Descrição')),
                ('description_en', models.TextField(blank=True, verbose_name='Descrição')),
                ('status', models.CharField(choices=[('opened', 'Aberta'), ('done', 'Concluída')], max_length=6, verbose_name='Status')),
                ('mobilization_id', models.IntegerField(blank=True, null=True, verbose_name='ID da Mobilização BONDE')),
                ('url', models.URLField(blank=True, null=True, verbose_name='Link da Campanha')),
                ('release_date', models.DateField(blank=True, null=True, verbose_name='Data de lançamento')),
                ('hide', models.BooleanField(default=False, verbose_name='Esconder')),
                ('campaign_group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='apps.campaigngroup', verbose_name='Comunidade')),
                ('header_image', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='campaign_header_image', to=settings.FILER_IMAGE_MODEL, verbose_name='Cabeçalho Imagem')),
                ('picture', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.FILER_IMAGE_MODEL, verbose_name='Imagem')),
                ('placeholder', cms.models.fields.PlaceholderField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, slotname='campaign_placeholder', to='cms.placeholder')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.site')),
                ('tags', tag_fields.managers.ModelTagsManager(help_text='A comma-separated list of tags.', through='tag_fields.ModelTagIntFk', to='tag_fields.ModelTag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Campanha',
            },
            managers=[
                ('on_site', django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
    ]
