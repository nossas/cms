# Generated by Django 3.2 on 2023-08-24 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eleicao', '0010_alter_eleicaocarousel_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='number',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Numero de voto'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='slug',
            field=models.SlugField(max_length=120, verbose_name='Seu link personalizado'),
        ),
        migrations.AlterField(
            model_name='pollingplace',
            name='place',
            field=models.CharField(max_length=120, verbose_name='Unidade do Conselho Tutelar'),
        ),
    ]