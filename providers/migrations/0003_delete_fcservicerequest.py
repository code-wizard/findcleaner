# Generated by Django 2.2.6 on 2019-10-23 04:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0002_fcservicerequest_service'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FcServiceRequest',
        ),
    ]
