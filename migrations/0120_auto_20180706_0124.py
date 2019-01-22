# Generated by Django 2.0.7 on 2018-07-05 17:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kuriocities', '0119_useractivityjournal_uploads'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('team', models.CharField(max_length=32)),
                ('message', models.TextField()),
                ('time', models.DateTimeField()),
                ('invitation', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kuriocities.Invitation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('invitation', 'user', 'time'),
            },
        ),
        migrations.AlterUniqueTogether(
            name='chatmessage',
            unique_together={('invitation', 'user', 'time')},
        ),
    ]
