# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-17 15:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kuriocities', '0039_auto_20171017_1653'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activity',
            old_name='translatabilityAreas',
            new_name='translatability_areas',
        ),
    ]
