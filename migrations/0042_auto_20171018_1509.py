# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-18 07:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kuriocities', '0041_auto_20171018_1348'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='activityquestion',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='activityquestion',
            name='activity',
        ),
        migrations.RemoveField(
            model_name='activityquestion',
            name='age_group',
        ),
        migrations.RemoveField(
            model_name='activityquestion',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='activityquestion',
            name='question',
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['activity', 'question_order', 'pk']},
        ),
        migrations.AddField(
            model_name='question',
            name='activity',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.PROTECT, to='kuriocities.Activity'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='age_groups',
            field=models.ManyToManyField(blank=True, to='kuriocities.AgeGroup'),
        ),
        migrations.AddField(
            model_name='question',
            name='avatar_bullet_1',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='avatar_bullet_2',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='question_order',
            field=models.IntegerField(blank=True, default=999),
        ),
        migrations.AddField(
            model_name='question',
            name='skill',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='kuriocities.Skill'),
        ),
        migrations.AddField(
            model_name='question',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='kuriocities.Subject'),
        ),
        migrations.AlterField(
            model_name='question',
            name='age_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='kuriocities.AgeGroup'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.TextField(),
        ),
        migrations.RemoveField(
            model_name='question',
            name='correct_answer',
        ),
        migrations.RemoveField(
            model_name='question',
            name='correct_answer_feedback',
        ),
        migrations.RemoveField(
            model_name='question',
            name='curriculum',
        ),
        migrations.RemoveField(
            model_name='question',
            name='execution',
        ),
        migrations.RemoveField(
            model_name='question',
            name='objectives',
        ),
        migrations.RemoveField(
            model_name='question',
            name='potential_answer',
        ),
        migrations.RemoveField(
            model_name='question',
            name='skills',
        ),
        migrations.RemoveField(
            model_name='question',
            name='subjects',
        ),
        migrations.RemoveField(
            model_name='question',
            name='wrong_answer_feedback',
        ),
        migrations.AlterUniqueTogether(
            name='question',
            unique_together=set([('activity', 'question')]),
        ),
        migrations.DeleteModel(
            name='ActivityQuestion',
        ),
    ]