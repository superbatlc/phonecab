# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='kind',
            field=models.IntegerField(default=0, choices=[(0, b'utente'), (1, b'numero autorizzato'), (2, b'credito')]),
            preserve_default=True,
        ),
    ]
