# Generated by Django 4.2 on 2024-08-30 23:17

from django.db import migrations, models
import django.db.models.deletion
import filer.fields.file


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('filer', '0017_image__transparent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome da Parceria')),
                ('link', models.URLField(blank=True, null=True, verbose_name='Link da Parceria')),
                ('logo', filer.fields.file.FilerFileField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='filer.file', verbose_name='Imagem')),
            ],
            options={
                'verbose_name': 'Parceiro',
            },
        ),
    ]
