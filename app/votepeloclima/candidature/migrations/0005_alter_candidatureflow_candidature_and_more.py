# Generated by Django 4.2 on 2024-07-09 19:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('candidature', '0004_alter_candidatureflow_properties'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidatureflow',
            name='candidature',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='candidature.candidature'),
        ),
        migrations.AlterField(
            model_name='candidatureflow',
            name='status',
            field=models.CharField(choices=[('draft', 'Editando'), ('submitted', 'Enviado'), ('invalid', 'Inválido'), ('is_valid', 'Válido'), ('draft_requested', 'Edição Requisitada')], default='draft', max_length=50),
        ),
    ]