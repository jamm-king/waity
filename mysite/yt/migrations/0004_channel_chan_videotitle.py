# Generated by Django 3.2.6 on 2022-07-18 07:14

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('yt', '0003_channel_chan_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='chan_videoTitle',
            field=django_mysql.models.ListCharField(models.CharField(max_length=300), default=[], max_length=1505, size=5),
        ),
    ]
