# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-23 16:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kuriocities', '0021_auto_20170923_2342'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activity',
            old_name='city',
            new_name='cities',
        ),
        migrations.RenameField(
            model_name='activity',
            old_name='context',
            new_name='contexts',
        ),
        migrations.RenameField(
            model_name='activity',
            old_name='job',
            new_name='jobs',
        ),
        migrations.RenameField(
            model_name='activity',
            old_name='location',
            new_name='locations',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='skill',
            new_name='skills',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='subject',
            new_name='subjects',
        ),
    ]
