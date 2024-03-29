# Generated by Django 4.2 on 2024-03-12 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        ('plugins', '0032_merge_20240304_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='fullpageslider',
            name='x_and_y_center',
            field=models.BooleanField(default=False, verbose_name='Alinhar todo o conteúdo ao centro'),
        ),
        migrations.AlterField(
            model_name='accordionitem',
            name='cmsplugin_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='%(app_label)s_%(class)s', serialize=False, to='cms.cmsplugin'),
        ),
        migrations.AlterField(
            model_name='box',
            name='cmsplugin_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='%(app_label)s_%(class)s', serialize=False, to='cms.cmsplugin'),
        ),
        migrations.AlterField(
            model_name='breadcrumb',
            name='cmsplugin_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='%(app_label)s_%(class)s', serialize=False, to='cms.cmsplugin'),
        ),
        migrations.AlterField(
            model_name='breadcrumb',
            name='graphic_icon',
            field=models.CharField(blank=True, choices=[('questionador', 'Questionador'), ('hub', 'Hub, Eixo'), ('impulsionador', 'Impulsionador'), ('impacto', 'Impacto'), ('empatico', 'Empático')], max_length=50, null=True, verbose_name='Ícone gráfico'),
        ),
        migrations.AlterField(
            model_name='button',
            name='cmsplugin_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='%(app_label)s_%(class)s', serialize=False, to='cms.cmsplugin'),
        ),
        migrations.AlterField(
            model_name='card',
            name='cmsplugin_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='%(app_label)s_%(class)s', serialize=False, to='cms.cmsplugin'),
        ),
        migrations.AlterField(
            model_name='card',
            name='external_link',
            field=models.CharField(blank=True, help_text='Forneça um link para uma fonte externa.', max_length=2040, verbose_name='Link externo'),
        ),
        migrations.AlterField(
            model_name='card',
            name='internal_link',
            field=models.ForeignKey(blank=True, help_text='Se fornecido, substitui o link externo.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='cms.page', verbose_name='Link interno'),
        ),
        migrations.AlterField(
            model_name='card',
            name='target',
            field=models.CharField(blank=True, choices=[('_blank', 'Abrir em nova janela'), ('_self', 'Abrir na mesma janela')], max_length=255, verbose_name='Target'),
        ),
        migrations.AlterField(
            model_name='column',
            name='cmsplugin_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='%(app_label)s_%(class)s', serialize=False, to='cms.cmsplugin'),
        ),
        migrations.AlterField(
            model_name='container',
            name='cmsplugin_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='%(app_label)s_%(class)s', serialize=False, to='cms.cmsplugin'),
        ),
        migrations.AlterField(
            model_name='fullpageslider',
            name='cmsplugin_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='%(app_label)s_%(class)s', serialize=False, to='cms.cmsplugin'),
        ),
        migrations.AlterField(
            model_name='grid',
            name='cmsplugin_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='%(app_label)s_%(class)s', serialize=False, to='cms.cmsplugin'),
        ),
        migrations.AlterField(
            model_name='header',
            name='cmsplugin_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='%(app_label)s_%(class)s', serialize=False, to='cms.cmsplugin'),
        ),
        migrations.AlterField(
            model_name='headerimage',
            name='cmsplugin_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='%(app_label)s_%(class)s', serialize=False, to='cms.cmsplugin'),
        ),
        migrations.AlterField(
            model_name='headerimage',
            name='graphic_icon',
            field=models.CharField(blank=True, choices=[('questionador', 'Questionador'), ('hub', 'Hub, Eixo'), ('impulsionador', 'Impulsionador'), ('impacto', 'Impacto'), ('empatico', 'Empático')], max_length=50, null=True, verbose_name='Ícone gráfico'),
        ),
        migrations.AlterField(
            model_name='headline',
            name='cmsplugin_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='%(app_label)s_%(class)s', serialize=False, to='cms.cmsplugin'),
        ),
        migrations.AlterField(
            model_name='navbar',
            name='cmsplugin_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='%(app_label)s_%(class)s', serialize=False, to='cms.cmsplugin'),
        ),
        migrations.AlterField(
            model_name='pdfviewer',
            name='cmsplugin_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='%(app_label)s_%(class)s', serialize=False, to='cms.cmsplugin'),
        ),
        migrations.AlterField(
            model_name='socialsharepluginmodel',
            name='cmsplugin_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='%(app_label)s_%(class)s', serialize=False, to='cms.cmsplugin'),
        ),
    ]
