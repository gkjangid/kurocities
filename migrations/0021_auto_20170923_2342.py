# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-23 15:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kuriocities', '0020_remove_activity_age_group'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activity',
            old_name='previous_Activity',
            new_name='previous_activity',
        ),
    ]