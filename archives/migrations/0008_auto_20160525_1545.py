# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archives', '0007_archivedwhitelist_lawyer'),
    ]

    operations = [
        migrations.AddField(
            model_name='archiveddetail',
            name='lawyer',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='archivedphoneuser',
            name='additional_calls',
            field=models.BooleanField(default=False, verbose_name=b'chiamate supplementari'),
            preserve_default=True,
        ),
    ]
