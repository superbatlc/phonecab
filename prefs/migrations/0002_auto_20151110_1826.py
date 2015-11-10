# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prefs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fare',
            name='icon',
            field=models.CharField(default=b'zmdi zmdi-home', max_length=50),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fare',
            name='visible',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
