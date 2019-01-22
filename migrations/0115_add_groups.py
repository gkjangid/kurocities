# Generated by Django 2.0.3 on 2018-05-21 09:18

from django.db import migrations

def add_groups( apps, schema_editor ) -> None:
    groups = [
        'KCT-Activity-Enroll',
        'KCT-Activity-Invite',
        'KCT-Activity-Send',
        'KCT-Previewer',
    ]
    model = apps.get_model( 'auth', 'Group' )
    for group in groups:
        model.objects.get_or_create( name=group )


class Migration(migrations.Migration):

    dependencies = [
        ('kuriocities', '0114_auto_20180411_1343'),
    ]

    operations = [
        migrations.RunPython( add_groups, migrations.RunPython.noop ),
    ]