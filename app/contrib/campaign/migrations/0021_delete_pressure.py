# Generated by Django 3.2 on 2023-07-06 20:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        ('campaign', '0020_rename_widget_pressure_widget_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Pressure',
        ),
    ]
