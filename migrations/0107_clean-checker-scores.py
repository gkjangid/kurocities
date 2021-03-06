# Generated by Django 2.0.2 on 2018-03-01 16:54

from django.db import migrations

def needs_checker( question ):
    return question ['questionType'] == 'noAutoCorrection' and question.get( 'needsChecker' )

def clean_score( apps, schema_editor ):
    UserActivity = apps.get_model( 'kuriocities', 'UserActivity' )
    for ua in UserActivity.objects.all():
        questions = ua.activity.data ['questions']
        for qIdx, question in enumerate( questions ):
            if needs_checker( question ):
                scores = ua.scores.get( 'questions' )
                if not scores: continue
                score = scores [ str( qIdx ) ]
                if score [0] == 0:
                    score [1] = 0
                ua.save()



class Migration(migrations.Migration):

    dependencies = [
        ('kuriocities', '0106_convert-scores'),
    ]

    operations = [
        migrations.RunPython( clean_score, migrations.RunPython.noop ),
    ]
