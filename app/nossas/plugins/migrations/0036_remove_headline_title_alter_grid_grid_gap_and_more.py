# Generated by Django 4.2 on 2024-04-25 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plugins', '0035_grid_grid_layout_mobile_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='headline',
            name='title',
        ),
        migrations.AlterField(
            model_name='grid',
            name='grid_gap',
            field=models.CharField(choices=[('row-gap: 0;', 'Sem espaçamento'), ('row-gap: 4;', 'Pequeno'), ('row-gap: 8;', 'Grande')], default='row-gap: 4;', help_text='Selecione o espaço entre linhas e colunas do Grid.', max_length=15, verbose_name='Espaçamento do Grid'),
        ),
        migrations.AlterField(
            model_name='grid',
            name='grid_layout',
            field=models.CharField(choices=[(' ', 'Auto'), ('g-col-12', '1 Coluna'), ('g-col-12 g-col-md-6', '2 Colunas'), ('g-col-12 g-col-md-4', '3 Colunas'), ('g-col-12 g-col-md-3', '4 Colunas'), ('g-col-12 g-col-md-2', '6 Colunas'), ('g-col-12 g-col-md-1', '12 Colunas')], default='g-col-12 g-col-md-3', help_text='Defina o número de colunas para a visualização da página.', max_length=80, verbose_name='Layout do Grid'),
        ),
        migrations.AlterField(
            model_name='grid',
            name='grid_layout_mobile',
            field=models.CharField(choices=[(' ', 'Auto'), ('g-col-12', '1 Coluna'), ('g-col-12 g-col-md-6', '2 Colunas'), ('g-col-12 g-col-md-4', '3 Colunas'), ('g-col-12 g-col-md-3', '4 Colunas'), ('g-col-12 g-col-md-2', '6 Colunas'), ('g-col-12 g-col-md-1', '12 Colunas')], default='g-col-12', help_text='Selecione o número de colunas para exibição da página em dispositivos móveis.', max_length=80, verbose_name='Layout do Grid Mobile'),
        ),
    ]