# Generated by Django 2.0.7 on 2018-10-10 07:15

from django.db import migrations


def add_objects( apps, schema_editor ):
    names = [
        'Messaging',
        'Team',
        'Activity-Journal',
        'General-Journal-Question',
    ]
    model   = apps.get_model( 'kuriocities', 'AppFeature' )
    objects = [ model( name = name ) for name in names ]
    model.objects.bulk_create( objects )

class Migration(migrations.Migration):

    dependencies = [
        ('kuriocities', '0133_appfeature'),
    ]

    operations = [
        migrations.RunPython( add_objects, migrations.RunPython.noop ),
    ]