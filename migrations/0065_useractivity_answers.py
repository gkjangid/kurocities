# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-04 18:42
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kuriocities', '0064_useractivity_actions'),
    ]

    operations = [
        migrations.AddField(
            model_name='useractivity',
            name='answers',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=[]),
        ),
    ]