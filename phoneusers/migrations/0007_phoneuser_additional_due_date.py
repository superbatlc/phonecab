# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phoneusers', '0006_auto_20160701_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='phoneuser',
            name='additional_due_date',
            field=models.DateTimeField(null=True, verbose_name=b'scadenza chiamate supplementari'),
        ),
    ]
