# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-09 21:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fpagecse', '0004_auto_20171109_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faculty',
            name='department',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='room_no',
            field=models.CharField(default='', max_length=20),
        ),
    ]
