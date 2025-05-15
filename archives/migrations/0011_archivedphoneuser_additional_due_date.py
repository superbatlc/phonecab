# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archives', '0010_auto_20160603_1658'),
    ]

    operations = [
        migrations.AddField(
            model_name='archivedphoneuser',
            name='additional_due_date',
            field=models.DateTimeField(null=True, verbose_name=b'scadenza chiamate supplementari'),
        ),
    ]
