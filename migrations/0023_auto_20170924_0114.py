# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-23 17:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kuriocities', '0022_auto_20170924_0029'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='objectives',
        ),
        migrations.AddField(
            model_name='question',
            name='objectives',
            field=models.ManyToManyField(blank=True, to='kuriocities.LearningObjectives'),
        ),
    ]
