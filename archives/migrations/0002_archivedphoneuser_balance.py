# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archives', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='archivedphoneuser',
            name='balance',
            field=models.DecimalField(default=0, verbose_name=b'credito residuo', max_digits=5, decimal_places=2),
            preserve_default=True,
        ),
    ]
