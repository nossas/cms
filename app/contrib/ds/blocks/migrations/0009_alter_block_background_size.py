# Generated by Django 4.2 on 2024-05-17 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0008_alter_block_background_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='background_size',
            field=models.CharField(choices=[('cover', 'Preencher Área'), ('contain', 'Redimensionar'), ('initial', 'Tamanho Original')], default='cover', help_text='Escolha como a imagem de fundo deve ser exibida', max_length=8, verbose_name='Tamanho'),
        ),
    ]
