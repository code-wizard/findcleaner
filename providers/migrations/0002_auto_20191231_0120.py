# Generated by Django 2.2.6 on 2019-12-31 01:20

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fcprovider',
            name='coords',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), default=(0,0), size=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fcprovider',
            name='type',
            field=models.CharField(choices=[('individual', 'Individual'), ('Agency', 'Agency')], default='individual', max_length=10),
        ),
    ]