# Generated by Django 2.0.2 on 2018-03-07 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kuriocities', '0110_create-group-reviewer'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='change_password',
            field=models.BooleanField(default=False),
        ),
    ]
