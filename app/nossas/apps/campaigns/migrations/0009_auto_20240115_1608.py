# Generated by Django 3.2 on 2024-01-15 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0008_campaign_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='release_date',
            field=models.DateField(blank=True, null=True, verbose_name='Data de lançamento da Campanha'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='hide',
            field=models.BooleanField(default=False, verbose_name='Esconder Campanha'),
        ),
    ]