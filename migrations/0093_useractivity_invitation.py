# Generated by Django 2.0.2 on 2018-02-13 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kuriocities', '0092_auto_20180208_1035'),
    ]

    operations = [
        migrations.AddField(
            model_name='useractivity',
            name='invitation',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='kuriocities.Invitation'),
        ),
    ]