# Generated by Django 3.2 on 2023-11-28 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eleicao', '0019_auto_20231123_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eleicaocandidatelist',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Descrição'),
        ),
    ]
