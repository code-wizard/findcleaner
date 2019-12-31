# Generated by Django 2.2.6 on 2019-12-31 04:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0006_fcprovider_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fcprovider',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='provider_info', to=settings.AUTH_USER_MODEL),
        ),
    ]
