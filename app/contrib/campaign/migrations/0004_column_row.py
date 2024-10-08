# Generated by Django 3.2 on 2023-05-19 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        ('campaign', '0003_actionbutton'),
    ]

    operations = [
        migrations.CreateModel(
            name='Column',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='campaign_column', serialize=False, to='cms.cmsplugin')),
                ('classnames', models.CharField(choices=[('flex-auto', 'Auto')], default='flex-auto', max_length=20, verbose_name='Estilho da coluna')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='Row',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='campaign_row', serialize=False, to='cms.cmsplugin')),
                ('classnames', models.CharField(choices=[('flex flex-flow-col', 'Flex')], default='flex flex-flow-col', max_length=20, verbose_name='Estilo da linha')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
