# Generated by Django 3.2 on 2023-10-20 18:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landpage', '0008_auto_20231020_1841'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carouselplugin',
            name='description',
        ),
        migrations.RemoveField(
            model_name='carouselplugin',
            name='title',
        ),
    ]
