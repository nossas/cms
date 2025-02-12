# Generated by Django 4.2 on 2024-03-18 19:01

from django.db import migrations
import tag_fields.managers


class Migration(migrations.Migration):

    dependencies = [
        ('tag_fields', '0001_initial'),
        ('publications', '0002_remove_publication_classification_publication_parent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='tags',
            field=tag_fields.managers.ModelTagsManager(blank=True, help_text='A comma-separated list of tags.', through='tag_fields.ModelTagIntFk', to='tag_fields.ModelTag', verbose_name='Tags'),
        ),
    ]
