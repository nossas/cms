# Generated by Django 3.2 on 2023-08-02 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eleicao', '0011_alter_candidate_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='neighborhood',
            field=models.CharField(max_length=80, verbose_name='Bairro'),
        ),
    ]