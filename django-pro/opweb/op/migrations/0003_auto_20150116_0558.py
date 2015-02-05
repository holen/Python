# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('op', '0002_auto_20150116_0557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='load',
            name='load_update_date',
            field=models.DateField(),
            preserve_default=True,
        ),
    ]
