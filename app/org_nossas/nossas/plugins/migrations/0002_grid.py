# Generated by Django 3.2 on 2024-01-11 20:48

from django.db import migrations, models
import django.db.models.deletion
import org_nossas.nossas.design.models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        ('plugins', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grid',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='plugins_grid', serialize=False, to='cms.cmsplugin')),
                ('attributes', models.JSONField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(org_nossas.nossas.design.models.UIBackgroundMixin, 'cms.cmsplugin'),
        ),
    ]
