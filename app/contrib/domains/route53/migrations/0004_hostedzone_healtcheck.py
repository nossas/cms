# Generated by Django 4.2.6 on 2023-11-06 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('route53', '0003_recordset'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostedzone',
            name='healtcheck',
            field=models.BooleanField(default=False),
        ),
    ]
