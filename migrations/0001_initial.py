# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-12 15:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField()),
                ('picture_url', models.URLField(blank=True, default='')),
                ('video_url', models.URLField(blank=True, default='')),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('dates_comment', models.TextField(blank=True, default='')),
                ('first_session', models.TimeField()),
                ('last_session', models.TimeField()),
                ('times_comment', models.TextField(blank=True, default='')),
                ('sponsored', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')])),
                ('curriculum', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], verbose_name='Official Curriculum')),
            ],
            options={
                'verbose_name_plural': 'Activities',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='AgeGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('order', models.IntegerField(blank=True, default=999)),
            ],
            options={
                'ordering': ['order', 'id', 'name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('order', models.IntegerField(blank=True, default=999)),
            ],
            options={
                'verbose_name_plural': 'Cities',
                'ordering': ['order', 'name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Context',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('order', models.IntegerField(blank=True, default=999)),
            ],
            options={
                'ordering': ['order', 'name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('order', models.IntegerField(blank=True, default=999)),
            ],
            options={
                'ordering': ['order', 'id', 'name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Curriculum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('order', models.IntegerField(blank=True, default=999)),
            ],
            options={
                'verbose_name_plural': 'Curricula',
                'ordering': ['order', 'name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Duration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('order', models.IntegerField(blank=True, default=999)),
            ],
            options={
                'ordering': ['order', 'id', 'name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Execution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('order', models.IntegerField(blank=True, default=999)),
            ],
            options={
                'ordering': ['order', 'name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('order', models.IntegerField(blank=True, default=999)),
            ],
            options={
                'ordering': ['order', 'name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('order', models.IntegerField(blank=True, default=999)),
                ('address', models.TextField()),
                ('website', models.URLField(blank=True, default='')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kuriocities.City')),
            ],
            options={
                'ordering': ['order', 'name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255, unique=True)),
                ('potential_answer', models.CharField(blank=True, default='', max_length=255)),
                ('correct_answer', models.CharField(blank=True, default='', max_length=255)),
                ('objectives', models.TextField()),
                ('age_group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kuriocities.AgeGroup')),
                ('curriculum', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kuriocities.Curriculum')),
                ('execution', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kuriocities.Execution')),
                ('job', models.ManyToManyField(to='kuriocities.Job')),
            ],
            options={
                'ordering': ['question'],
            },
        ),
        migrations.CreateModel(
            name='QuestionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('order', models.IntegerField(blank=True, default=999)),
            ],
            options={
                'ordering': ('validation_type', 'order', 'name'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SequenceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('order', models.IntegerField(blank=True, default=999)),
            ],
            options={
                'ordering': ['order', 'name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Situation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('order', models.IntegerField(blank=True, default=999)),
            ],
            options={
                'ordering': ['order', 'name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('order', models.IntegerField(blank=True, default=999)),
            ],
            options={
                'ordering': ['order', 'name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('order', models.IntegerField(blank=True, default=999)),
            ],
            options={
                'ordering': ['order', 'name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ValidationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('order', models.IntegerField(blank=True, default=999)),
            ],
            options={
                'ordering': ['order', 'name'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='questiontype',
            name='validation_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kuriocities.ValidationType'),
        ),
        migrations.AddField(
            model_name='question',
            name='question_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kuriocities.QuestionType'),
        ),
        migrations.AddField(
            model_name='question',
            name='sequence_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kuriocities.SequenceType'),
        ),
        migrations.AddField(
            model_name='question',
            name='skill',
            field=models.ManyToManyField(to='kuriocities.Skill'),
        ),
        migrations.AddField(
            model_name='question',
            name='subject',
            field=models.ManyToManyField(to='kuriocities.Subject'),
        ),
        migrations.AddField(
            model_name='question',
            name='validation_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kuriocities.ValidationType'),
        ),
        migrations.AddField(
            model_name='activity',
            name='city',
            field=models.ManyToManyField(to='kuriocities.City'),
        ),
        migrations.AddField(
            model_name='activity',
            name='context',
            field=models.ManyToManyField(to='kuriocities.Context'),
        ),
        migrations.AddField(
            model_name='activity',
            name='cost',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kuriocities.Cost'),
        ),
        migrations.AddField(
            model_name='activity',
            name='duration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kuriocities.Duration'),
        ),
        migrations.AddField(
            model_name='activity',
            name='job',
            field=models.ManyToManyField(to='kuriocities.Job'),
        ),
        migrations.AddField(
            model_name='activity',
            name='location',
            field=models.ManyToManyField(to='kuriocities.Location'),
        ),
        migrations.AddField(
            model_name='activity',
            name='situation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kuriocities.Situation'),
        ),
        migrations.AddField(
            model_name='activity',
            name='skill',
            field=models.ManyToManyField(to='kuriocities.Skill'),
        ),
        migrations.AddField(
            model_name='activity',
            name='subject',
            field=models.ManyToManyField(to='kuriocities.Subject'),
        ),
        migrations.AddField(
            model_name='activity',
            name='validation_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kuriocities.ValidationType'),
        ),
    ]
