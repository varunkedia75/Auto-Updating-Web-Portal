# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-18 16:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fpagecse', '0018_auto_20171115_1920'),
    ]

    operations = [
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=200)),
                ('degree', models.CharField(max_length=30)),
                ('supervisor', models.CharField(max_length=200)),
                ('scholar_name', models.CharField(max_length=200)),
                ('thesis_title', models.CharField(max_length=200)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
