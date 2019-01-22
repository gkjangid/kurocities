# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-23 16:20
from __future__ import unicode_literals

from django.db import migrations

def fix_missing_data_fields( apps, schema_editor ):
    Activity = apps.get_model( 'kuriocities', 'Activity' )
    for activity in Activity.objects.all():
        activity.data.setdefault( 'questions', [] )
        activity.data.setdefault( 'backboneType', 'activity' )
        activity.save()


class Migration(migrations.Migration):

    dependencies = [
        ('kuriocities', '0054_auto_20171023_1704'),
    ]

    operations = [
        migrations.RunPython( fix_missing_data_fields, migrations.RunPython.noop ),
    ]
