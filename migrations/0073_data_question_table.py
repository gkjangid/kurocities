# Generated by Django 2.0 on 2017-12-13 10:00

from django.db import migrations


def add_question_table( apps, schema_editor ):
    model = apps.get_model( 'kuriocities', 'Activity' )
    for activity in model.objects.order_by( 'modified' ):
        for question in activity.data.get( 'questions', [] ):
            if 'table' not in question:
                question['table'] = {
                    'rows':     [],
                    'columns':  [],
                }
            activity.save()

class Migration(migrations.Migration):

    dependencies = [
        ('kuriocities', '0072_data_choice_order'),
    ]

    operations = [
        migrations.RunPython( add_question_table, migrations.RunPython.noop ),
    ]
