# Generated by Django 2.0.7 on 2018-08-21 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kuriocities', '0125_auto_20180820_1454'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='learningjournal',
            name='activity',
        ),
        migrations.AddField(
            model_name='activity',
            name='learning_journal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='kuriocities.LearningJournal'),
        ),
    ]