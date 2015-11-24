# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archives', '0003_archivedcredit_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='archiveddetail',
            name='custom_valid',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
