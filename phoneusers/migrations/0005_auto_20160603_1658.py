# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phoneusers', '0004_auto_20160525_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phoneuser',
            name='additional_calls',
            field=models.IntegerField(default=0, verbose_name=b'chiamate supplementari'),
        ),
    ]
