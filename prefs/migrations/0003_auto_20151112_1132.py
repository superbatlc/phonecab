# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prefs', '0002_auto_20151110_1826'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fare',
            name='visible',
        ),
        migrations.AddField(
            model_name='fare',
            name='position',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
