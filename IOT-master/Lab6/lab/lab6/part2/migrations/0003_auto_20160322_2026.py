# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-22 20:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('part2', '0002_remove_city_temperature'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('city', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('latitude', models.CharField(max_length=30)),
                ('longitude', models.CharField(max_length=30)),
                ('temperature', models.CharField(max_length=30)),
            ],
        ),
        migrations.DeleteModel(
            name='City',
        ),
    ]
