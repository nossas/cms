# Generated by Django 4.2 on 2024-09-03 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidature', '0018_alter_candidature_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidature',
            name='intended_position',
            field=models.CharField(choices=[('', 'Selecione uma opção'), ('prefeitura', 'Prefeito/a'), ('vereacao', 'Vereador/a')], max_length=50, verbose_name='Cargo Pretendido'),
        ),
    ]