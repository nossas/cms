# Generated by Django 4.2 on 2024-05-02 14:13

from django.db import migrations
import django_jsonform.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ds', '0003_remove_theme_scss_theme_scss_json'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theme',
            name='scss_json',
            field=django_jsonform.models.fields.JSONField(blank=True, null=True),
        ),
    ]
