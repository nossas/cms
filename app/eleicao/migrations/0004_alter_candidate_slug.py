# Generated by Django 3.2 on 2023-08-01 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eleicao', '0003_candidate_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='slug',
            field=models.SlugField(max_length=120, unique=True, verbose_name='Slug'),
        ),
    ]