# Generated by Django 3.2 on 2024-01-17 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plugins', '0009_container'),
    ]

    operations = [
        migrations.AlterField(
            model_name='column',
            name='alignment_x',
            field=models.CharField(choices=[('align-items: start;', 'Acima'), ('align-items: center;', 'Ao centro'), ('align-items: end;', 'Abaixo')], default='align-items: start;', max_length=50, verbose_name='Alinhamento horizontal'),
        ),
        migrations.AlterField(
            model_name='column',
            name='alignment_y',
            field=models.CharField(choices=[('justify-content: left;', 'Esquerda'), ('justify-content: center;', 'Centralizar'), ('justify-content: right;', 'Direita')], default='justify-content: left;', max_length=50, verbose_name='Alinhamento vertical'),
        ),
    ]