# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0007_auto_20160701_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='calldate',
            field=models.DateTimeField(verbose_name=datetime.datetime(2016, 12, 20, 15, 52, 15, 55641)),
        ),
    ]
