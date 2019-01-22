# Generated by Django 2.0.7 on 2018-10-08 06:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kuriocities', '0129_auto_20180912_2033'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=256)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='kuriocities.Category')),
            ],
            options={
                'ordering': ('parent', 'name'),
            },
        ),
        migrations.AlterField(
            model_name='activity',
            name='checker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='checker_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('parent', 'name')},
        ),
    ]