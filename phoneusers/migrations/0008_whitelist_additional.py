# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phoneusers', '0007_phoneuser_additional_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='whitelist',
            name='additional',
            field=models.BooleanField(default=False, verbose_name=b'abilitazione a supplementari'),
        ),
    ]
