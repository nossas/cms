# Generated by Django 4.2 on 2024-09-02 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='partner',
            options={'ordering': ['position'], 'verbose_name': 'Parceiro'},
        ),
        migrations.AddField(
            model_name='partner',
            name='position',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
