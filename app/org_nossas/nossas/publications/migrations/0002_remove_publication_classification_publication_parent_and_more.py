# Generated by Django 4.2 on 2024-03-18 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        ('publications', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publication',
            name='classification',
        ),
        migrations.AddField(
            model_name='publication',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cms.page', verbose_name='Página Relacionada'),
        ),
        migrations.DeleteModel(
            name='Classification',
        ),
    ]
