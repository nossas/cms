# Generated by Django 4.2 on 2024-04-10 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grid', '0003_column_start'),
    ]

    operations = [
        migrations.AddField(
            model_name='grid',
            name='alignment',
            field=models.CharField(blank=True, choices=[('start', 'Start'), ('center', 'Center'), ('end', 'End')], max_length=6, null=True),
        ),
    ]