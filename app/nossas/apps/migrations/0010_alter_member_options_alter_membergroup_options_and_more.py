# Generated by Django 4.2 on 2024-03-04 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0009_member_my_order_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='member',
            options={'ordering': ('my_order', 'full_name'), 'verbose_name': 'Colaborador'},
        ),
        migrations.AlterModelOptions(
            name='membergroup',
            options={'ordering': ('my_order',), 'verbose_name': 'Equipe'},
        ),
        migrations.AddField(
            model_name='membergroup',
            name='my_order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]