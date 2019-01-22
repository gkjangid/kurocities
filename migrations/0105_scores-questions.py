# Generated by Django 2.0.2 on 2018-03-01 12:11

from django.db import migrations


def rename_key( apps, schema_editor ):
    UserActivity = apps.get_model( 'kuriocities', 'UserActivity' )
    for user_activity in UserActivity.objects.all():
        if '_questions' in user_activity.scores:
            user_activity.scores ['questions'] = user_activity.scores.pop( '_questions' )
            user_activity.save()

class Migration(migrations.Migration):

    dependencies = [
        ('kuriocities', '0104_auto_20180301_1329'),
    ]

    operations = [
        migrations.RunPython( rename_key, migrations.RunPython.noop ),
    ]