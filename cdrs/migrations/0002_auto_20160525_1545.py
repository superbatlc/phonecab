# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdrs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='superbacdr',
            name='lawyer',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='superbacdr',
            name='calltype',
            field=models.IntegerField(default=0, choices=[(0, b'ordinaria'), (1, b'straordinaria'), (2, b'speciale')]),
        ),
    ]
