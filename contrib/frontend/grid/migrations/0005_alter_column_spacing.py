# Generated by Django 3.2 on 2023-06-14 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grid', '0004_column_spacing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='column',
            name='spacing',
            field=models.CharField(choices=[('gap-0', 'Sem espaçamento'), ('gap-4', 'Pequeno'), ('gap-8', 'Grande')], default='gap-0', help_text='Espaço entre os elementos desta Coluna', max_length=15, verbose_name='Espaçamento'),
        ),
    ]