# Generated by Django 2.0 on 2018-01-27 07:29

from django.db import migrations

def capitalize( apps, schema_editor ):
    model = apps.get_model( 'kuriocities', 'LearningOutcomeVerb' )
    for row in model.objects.all():
        verb = row.verb.strip()
        row.verb = '%s%s' % (
            verb[0].upper(),
            verb[1:],
        )
        row.save()

class Migration(migrations.Migration):

    dependencies = [
        ('kuriocities', '0090_auto_20180117_1453'),
    ]

    operations = [ migrations.RunPython( capitalize, migrations.RunPython.noop ) ]