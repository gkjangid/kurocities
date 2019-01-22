# Generated by Django 2.0.7 on 2018-09-08 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kuriocities', '0126_auto_20180822_0119'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserActivityToDo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('question_no', models.IntegerField()),
                ('description', models.TextField()),
                ('message', models.TextField()),
                ('deadline', models.DateTimeField()),
                ('status', models.CharField(choices=[('in-progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='in-progress', max_length=30)),
                ('user_activity', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kuriocities.UserActivity')),
            ],
            options={
                'ordering': ('deadline', 'user_activity', 'question_no'),
            },
        ),
        migrations.AlterUniqueTogether(
            name='useractivitytodo',
            unique_together={('user_activity', 'question_no')},
        ),
    ]
