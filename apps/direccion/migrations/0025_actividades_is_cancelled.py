# Generated by Django 2.2.4 on 2019-10-08 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('direccion', '0024_auto_20191004_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='actividades',
            name='is_cancelled',
            field=models.BooleanField(default=False),
        ),
    ]
