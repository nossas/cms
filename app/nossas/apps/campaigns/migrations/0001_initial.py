# Generated by Django 3.2 on 2023-12-31 14:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=180)),
                ('description_pt_br', models.TextField(verbose_name='description')),
                ('description_en', models.TextField(blank=True, verbose_name='description')),
                ('status', models.CharField(choices=[('opened', 'Aberta'), ('closed', 'Fechada')], max_length=6)),
                ('picture', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.FILER_IMAGE_MODEL)),
            ],
        ),
    ]