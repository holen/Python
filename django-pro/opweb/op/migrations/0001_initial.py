# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Load',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('load_id', models.IntegerField(default=1)),
                ('load_server', models.CharField(max_length=200)),
                ('load_ip', models.CharField(max_length=15)),
                ('load_str', models.CharField(max_length=200)),
                ('load_ip_count', models.IntegerField(default=15)),
                ('load_update_date', models.DateField(default=datetime.datetime(2015, 1, 16, 5, 54, 9, 194816, tzinfo=utc))),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('machine_name', models.CharField(max_length=200)),
                ('machine_ip', models.CharField(max_length=15)),
                ('machine_user', models.CharField(max_length=200)),
                ('machine_passwd', models.CharField(max_length=200)),
                ('machine_update_date', models.DateField(default=datetime.datetime(2015, 1, 16, 5, 54, 9, 194407, tzinfo=utc))),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
