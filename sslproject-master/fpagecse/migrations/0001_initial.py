# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-08 11:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faculty_name', models.CharField(max_length=250)),
                ('designation', models.CharField(max_length=250)),
                ('photo', models.FileField(upload_to='')),
                ('phone', models.BigIntegerField()),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
