# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0010_auto_20190930_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='calldate',
            field=models.DateTimeField(verbose_name=datetime.datetime(2019, 9, 30, 14, 54, 18, 433940)),
        ),
    ]
