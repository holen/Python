# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('op', '0003_auto_20150116_0558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='load',
            name='load_update_date',
            field=models.DateField(verbose_name=b'update_time'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='machine',
            name='machine_update_date',
            field=models.DateField(verbose_name=b'last_update_time'),
            preserve_default=True,
        ),
    ]
