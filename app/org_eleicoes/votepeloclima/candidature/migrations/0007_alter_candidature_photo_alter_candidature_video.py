# Generated by Django 4.2 on 2024-07-30 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidature', '0006_alter_candidature_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidature',
            name='photo',
            field=models.FileField(blank=True, null=True, upload_to='candidatures/photos/'),
        ),
        migrations.AlterField(
            model_name='candidature',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='candidatures/videos/'),
        ),
    ]