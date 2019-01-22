# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-14 04:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kuriocities', '0030_auto_20171014_1149'),
    ]

    operations = [
        migrations.CreateModel(
            name='LearningOutcomeVerb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('category', models.CharField(choices=[('Comprehend', 'Comprehend'), ('Apply', 'Apply'), ('Analyze', 'Analyze'), ('Synthesize', 'Synthesize'), ('Evaluate', 'Evaluate'), ('Emotionalize', 'Emotionalize')], max_length=32)),
                ('verb', models.CharField(max_length=255)),
                ('order', models.IntegerField(blank=True, default=999)),
            ],
            options={
                'ordering': ['category', 'order', 'verb'],
            },
        ),
        migrations.DeleteModel(
            name='LearningOutcome',
        ),
        migrations.AlterUniqueTogether(
            name='learningoutcomeverb',
            unique_together=set([('category', 'verb')]),
        ),
    ]