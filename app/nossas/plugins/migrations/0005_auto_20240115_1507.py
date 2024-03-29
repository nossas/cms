# Generated by Django 3.2 on 2024-01-15 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plugins', '0004_auto_20240111_2221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='column',
            name='attributes',
        ),
        migrations.RemoveField(
            model_name='grid',
            name='attributes',
        ),
        migrations.AlterField(
            model_name='grid',
            name='grid_layout',
            field=models.CharField(choices=[(' ', 'Auto'), ('g-col-12', '1 Coluna'), ('g-col-12 g-col-md-6', '2 Colunas'), ('g-col-12 g-col-md-4', '3 Colunas'), ('g-col-12 g-col-md-3', '4 Colunas'), ('g-col-12 g-col-md-2', '6 Colunas'), ('g-col-12 g-col-md-1', '12 Colunas')], default=' ', help_text="Escolha 'Auto' para um layout responsivo automático ou para selecionar o número de colunas manualmente.", max_length=80, verbose_name='Layout do Grid'),
        ),
    ]
