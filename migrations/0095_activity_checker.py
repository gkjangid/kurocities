# Generated by Django 2.0.2 on 2018-02-15 03:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kuriocities', '0094_useractivityarchive'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='checker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='checker_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
