# Generated by Django 2.0.7 on 2018-10-08 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kuriocities', '0131_auto_20181008_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='score',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
