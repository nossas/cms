# Generated by Django 3.2 on 2023-08-01 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eleicao', '0002_auto_20230731_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='slug',
            field=models.SlugField(default='', max_length=120, verbose_name='Slug'),
            preserve_default=False,
        ),
    ]