# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-18 15:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kuriocities', '0005_auto_20170918_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='question',
            field=models.ManyToManyField(blank=True, to='kuriocities.Question'),
        ),
    ]
