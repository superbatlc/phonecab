# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0004_auto_20160527_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='calldate',
            field=models.DateTimeField(verbose_name=datetime.datetime(2016, 6, 3, 16, 58, 43, 84784)),
        ),
    ]
