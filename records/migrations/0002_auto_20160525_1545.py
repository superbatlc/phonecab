# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='calldate',
            field=models.DateTimeField(verbose_name=datetime.datetime(2016, 5, 25, 15, 45, 3, 201848)),
        ),
    ]
