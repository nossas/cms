# Generated by Django 3.2 on 2023-08-21 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eleicao', '0004_rename_referente_pollingplace_reference'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pollingplace',
            name='name',
        ),
        migrations.AddField(
            model_name='pollingplace',
            name='place',
            field=models.CharField(default='', max_length=120, verbose_name='Local'),
            preserve_default=False,
        ),
    ]