# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phoneusers', '0003_auto_20160525_1545'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='whitelist',
            name='frequency',
        ),
        migrations.AddField(
            model_name='whitelist',
            name='kind',
            field=models.IntegerField(default=0, verbose_name=b'tipologia', choices=[(0, b'Ordinaria'), (1, b'Primo ingresso')]),
            preserve_default=True,
        ),
    ]
