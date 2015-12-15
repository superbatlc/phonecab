# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archives', '0004_archiveddetail_custom_valid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivedphoneuser',
            name='balance',
            field=models.DecimalField(default=0, verbose_name=b'credito residuo', max_digits=7, decimal_places=4),
        ),
    ]
