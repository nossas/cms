# Generated by Django 3.2 on 2024-01-31 19:37

from django.db import migrations, models
import django.db.models.deletion
import filer.fields.file


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0017_image__transparent'),
        ('cms', '0022_auto_20180620_1551'),
        ('plugins', '0020_headerimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='headerimage',
            name='graphic_icon',
            field=models.CharField(blank=True, choices=[('hub', 'Hub, Eixo')], max_length=50, null=True, verbose_name='Ícone gráfico'),
        ),
        migrations.CreateModel(
            name='PDFViewer',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='plugins_pdfviewer', serialize=False, to='cms.cmsplugin')),
                ('file', filer.fields.file.FilerFileField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='filer.file')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]