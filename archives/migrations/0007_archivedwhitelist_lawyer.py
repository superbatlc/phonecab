# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archives', '0006_auto_20160301_0808'),
    ]

    operations = [
        migrations.AddField(
            model_name='archivedwhitelist',
            name='lawyer',
            field=models.BooleanField(default=False, verbose_name=b'avvocato'),
            preserve_default=True,
        ),
    ]
