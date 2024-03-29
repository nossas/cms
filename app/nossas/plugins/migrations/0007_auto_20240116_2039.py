# Generated by Django 3.2 on 2024-01-16 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plugins', '0006_merge_20240116_2039'),
    ]

    operations = [
        migrations.AddField(
            model_name='column',
            name='alignment_x',
            field=models.CharField(choices=[('justify-content: left;', 'Esquerda'), ('justify-content: center;', 'Centralizar'), ('justify-content: right;', 'Direita')], default='justify-content: left;', max_length=50, verbose_name='Alinhamento horizontal'),
        ),
        migrations.AddField(
            model_name='column',
            name='alignment_y',
            field=models.CharField(choices=[('align-items: start;', 'Acima'), ('align-items: center;', 'Ao centro'), ('align-items: end;', 'Abaixo')], default='align-items: start;', max_length=50, verbose_name='Alinhamento vertical'),
        ),
        migrations.AddField(
            model_name='column',
            name='spacing',
            field=models.CharField(choices=[('gap: 0;', 'Sem espaçamento'), ('gap: 4px;', 'Pequeno'), ('gap: 6px;', 'Médio'), ('gap: 8px;', 'Grande'), ('gap: 12px;', 'Muito Grande')], default='gap: 0;', help_text='Selecione o espaçamento dos itens dentro da coluna.', max_length=15, verbose_name='Espaçamento'),
        ),
    ]
