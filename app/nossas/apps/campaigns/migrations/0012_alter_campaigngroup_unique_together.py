# Generated by Django 3.2 on 2024-01-17 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('campaigns', '0011_auto_20240117_1535'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='campaigngroup',
            unique_together={('site', 'community_id')},
        ),
    ]