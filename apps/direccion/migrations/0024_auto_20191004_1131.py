# Generated by Django 2.2.4 on 2019-10-04 16:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('direccion', '0023_auto_20191004_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='correos_notificacion',
            name='usuario',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='correos', to=settings.AUTH_USER_MODEL),
        ),
    ]
