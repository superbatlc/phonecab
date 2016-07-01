# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phoneusers', '0005_auto_20160603_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='whitelist',
            name='duration',
            field=models.IntegerField(default=600, verbose_name=b'durata massima'),
        ),
    ]
