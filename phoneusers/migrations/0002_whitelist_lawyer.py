# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phoneusers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='whitelist',
            name='lawyer',
            field=models.BooleanField(default=False, verbose_name=b'avvocato'),
            preserve_default=True,
        ),
    ]
