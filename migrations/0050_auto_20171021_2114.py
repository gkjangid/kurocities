# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-21 13:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kuriocities', '0049_auto_20171021_2020'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='learningOutcome',
            new_name='learning_outcome',
        ),
    ]