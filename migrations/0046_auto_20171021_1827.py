# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-21 10:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kuriocities', '0045_auto_20171021_1709'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('order', models.IntegerField(blank=True, default=999)),
            ],
            options={
                'ordering': ['order', 'id'],
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='agegroup',
            options={'ordering': ['order', 'id']},
        ),
    ]
