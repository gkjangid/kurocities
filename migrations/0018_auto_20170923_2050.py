# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-23 12:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kuriocities', '0017_auto_20170923_2048'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('question_no', models.IntegerField()),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kuriocities.Activity')),
                ('age_group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kuriocities.AgeGroup')),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kuriocities.Question')),
            ],
            options={
                'ordering': ('activity', 'question_no'),
            },
        ),
        migrations.AlterUniqueTogether(
            name='activityquestion',
            unique_together=set([('activity', 'question'), ('activity', 'question_no')]),
        ),
    ]
