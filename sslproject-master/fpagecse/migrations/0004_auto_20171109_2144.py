# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-09 21:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fpagecse', '0003_auto_20171109_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faculty',
            name='password',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='username',
            field=models.CharField(default='', max_length=200),
        ),
    ]
