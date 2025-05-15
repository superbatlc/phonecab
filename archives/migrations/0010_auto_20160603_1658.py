# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archives', '0009_auto_20160525_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivedphoneuser',
            name='additional_calls',
            field=models.IntegerField(default=0, verbose_name=b'chiamate supplementari'),
        ),
    ]
