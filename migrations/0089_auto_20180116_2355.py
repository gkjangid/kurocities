# Generated by Django 2.0 on 2018-01-16 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kuriocities', '0088_auto_20180116_2240'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answerscore',
            old_name='points',
            new_name='score',
        ),
    ]
