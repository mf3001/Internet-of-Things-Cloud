# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-22 20:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('part2', '0003_auto_20160322_2026'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Cities',
            new_name='City',
        ),
    ]