# Generated by Django 2.0 on 2018-01-16 10:49

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kuriocities', '0084_auto_20180115_2041'),
    ]

    operations = [
        migrations.AddField(
            model_name='useractivity',
            name='scores',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict),
        ),
    ]
