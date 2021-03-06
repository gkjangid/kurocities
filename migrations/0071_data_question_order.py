# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-07 14:31
from __future__ import unicode_literals

from django.db import migrations


def set_order( apps, schema_editor ):
    model = apps.get_model( 'kuriocities', 'Activity' )
    for activity in model.objects.all():
        for i, question in enumerate( activity.data.get( 'questions', [] ) ):
            if question['questionOrder']  == 999:
                question['questionOrder'] = (i + 1) * 10
        activity.save()

class Migration(migrations.Migration):

    dependencies = [
        ('kuriocities', '0070_question_operands'),
    ]

    operations = [
        migrations.RunPython( set_order, migrations.RunPython.noop ),
    ]
