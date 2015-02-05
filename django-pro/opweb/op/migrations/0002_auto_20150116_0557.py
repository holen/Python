# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('op', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='load',
            name='load_update_date',
            field=models.DateField(default=datetime.datetime(2015, 1, 16, 5, 57, 45, 646440, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='machine',
            name='machine_update_date',
            field=models.DateField(verbose_name=b'pub_date'),
            preserve_default=True,
        ),
    ]
