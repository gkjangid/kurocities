# Generated by Django 2.0.7 on 2018-10-10 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kuriocities', '0132_category_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=32, unique=True)),
                ('enabled', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
