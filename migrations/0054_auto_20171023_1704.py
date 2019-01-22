# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-23 09:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kuriocities', '0053_save_activity_data'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='activityoutcome',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='activityoutcome',
            name='activity',
        ),
        migrations.RemoveField(
            model_name='activityoutcome',
            name='verb',
        ),
        migrations.RemoveField(
            model_name='answerchoice',
            name='question',
        ),
        migrations.AlterUniqueTogether(
            name='question',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='question',
            name='activity',
        ),
        migrations.RemoveField(
            model_name='question',
            name='age_groups',
        ),
        migrations.RemoveField(
            model_name='question',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='question',
            name='learning_outcome',
        ),
        migrations.RemoveField(
            model_name='question',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='question',
            name='question_type',
        ),
        migrations.RemoveField(
            model_name='question',
            name='skill',
        ),
        migrations.RemoveField(
            model_name='question',
            name='subject',
        ),
        migrations.AlterUniqueTogether(
            name='questionchoice',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='questionchoice',
            name='question',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='age_groups',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='avatar_bullet_1',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='avatar_bullet_2',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='brief_description',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='cities',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='contexts',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='cost',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='curriculum',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='dates_comment',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='description',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='execution',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='from_date',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='from_time',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='hours_24',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='jobs',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='locations',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='needs_coach',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='permanent_dates',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='picture_url',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='previous_activity',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='sequence_type',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='situation',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='sponsored',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='status',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='times_comment',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='to_date',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='to_time',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='translatability_areas',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='translatable',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='video_url',
        ),
        migrations.DeleteModel(
            name='ActivityOutcome',
        ),
        migrations.DeleteModel(
            name='AnswerChoice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.DeleteModel(
            name='QuestionChoice',
        ),
    ]
