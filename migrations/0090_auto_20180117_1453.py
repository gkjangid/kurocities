# Generated by Django 2.0 on 2018-01-17 06:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kuriocities', '0089_auto_20180116_2355'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='User',
            new_name='user',
        ),
    ]