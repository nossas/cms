# Generated by Django 3.2 on 2023-06-02 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0007_button'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='button',
            name='border_radius',
        ),
        migrations.AddField(
            model_name='button',
            name='rounded',
            field=models.CharField(blank=True, choices=[('rounded-sm', 'Small'), ('rounded', 'Padrão'), ('rounded-md', 'Medium'), ('rounded-lg', 'Large'), ('rounded-xl', 'Extra Large')], max_length=30, null=True, verbose_name='Arredondamento'),
        ),
        migrations.AlterField(
            model_name='button',
            name='border_size',
            field=models.CharField(blank=True, choices=[('border', 'Padrão (1px)'), ('border-0', 'Sem borda (0px)'), ('border-2', 'Pequeno (2px)'), ('border-4', 'Médio (4px)'), ('border-8', 'Grande (8px)')], max_length=30, null=True, verbose_name='Tamanho da borda'),
        ),
    ]