# Generated by Django 2.0.6 on 2018-06-28 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0002_auto_20180628_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]
