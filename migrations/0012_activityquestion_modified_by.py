# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-21 13:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kuriocities', '0011_auto_20170921_2050'),
    ]

    operations = [
        migrations.AddField(
            model_name='activityquestion',
            name='modified_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]