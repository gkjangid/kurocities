# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-19 03:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kuriocities', '0006_activity_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_no', models.IntegerField()),
            ],
            options={
                'ordering': ('activity', 'question_no'),
            },
        ),
        migrations.RemoveField(
            model_name='activity',
            name='question',
        ),
        migrations.AddField(
            model_name='activity',
            name='brief_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='activityquestion',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kuriocities.Activity'),
        ),
        migrations.AddField(
            model_name='activityquestion',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kuriocities.Question'),
        ),
        migrations.AlterUniqueTogether(
            name='activityquestion',
            unique_together=set([('activity', 'question'), ('activity', 'question_no')]),
        ),
    ]
