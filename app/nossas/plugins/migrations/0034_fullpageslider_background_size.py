# Generated by Django 4.2 on 2024-03-21 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plugins', '0033_fullpageslider_x_and_y_center_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fullpageslider',
            name='background_size',
            field=models.CharField(choices=[('contain', 'Contain'), ('cover', 'Cover'), ('initial', 'Initial')], default='contain', max_length=8),
            preserve_default=False,
        ),
    ]
