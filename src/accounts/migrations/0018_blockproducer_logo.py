# Generated by Django 2.0.7 on 2018-07-15 19:26

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_auto_20180713_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='blockproducer',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to=accounts.models.bp_logo_directory_path),
        ),
    ]
