# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-23 05:46
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kuriocities', '0051_auto_20171022_0221'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='data',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
    ]