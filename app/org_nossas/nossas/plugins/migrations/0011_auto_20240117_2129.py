# Generated by Django 3.2 on 2024-01-17 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plugins', '0010_auto_20240117_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='column',
            name='alignment_x',
            field=models.CharField(choices=[('align-items: start;', 'Esquerda'), ('align-items: center;', 'Centralizar'), ('align-items: end;', 'Direita')], default='align-items: start;', max_length=50, verbose_name='Alinhamento horizontal'),
        ),
        migrations.AlterField(
            model_name='column',
            name='alignment_y',
            field=models.CharField(choices=[('justify-content: left;', 'Acima'), ('justify-content: center;', 'Ao centro'), ('justify-content: right;', 'Abaixo')], default='justify-content: left;', max_length=50, verbose_name='Alinhamento vertical'),
        ),
        migrations.AlterField(
            model_name='column',
            name='col_start_at',
            field=models.CharField(choices=[(' ', 'Auto'), ('g-start-1', 'Start at Col 1'), ('g-start-2', 'Start at Col 2'), ('g-start-3', 'Start at Col 3'), ('g-start-4', 'Start at Col 4'), ('g-start-5', 'Start at Col 5'), ('g-start-6', 'Start at Col 6'), ('g-start-7', 'Start at Col 7'), ('g-start-8', 'Start at Col 8'), ('g-start-9', 'Start at Col 9'), ('g-start-10', 'Start at Col 10'), ('g-start-11', 'Start at Col 11'), ('g-start-12', 'Start at Col 12')], default=' ', help_text='Defina em qual coluna o elemento deve iniciar.', max_length=30, verbose_name='Inicio da coluna na linha'),
        ),
    ]