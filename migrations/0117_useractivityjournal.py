# Generated by Django 2.0.3 on 2018-06-01 02:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kuriocities', '0116_kct_activity_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserActivityJournal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('description', models.TextField()),
                ('user_activity', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kuriocities.UserActivity')),
            ],
            options={
                'ordering': ('user_activity', '-created'),
            },
        ),
    ]