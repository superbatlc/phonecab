# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phoneusers', '0002_whitelist_lawyer'),
    ]

    operations = [
        migrations.AddField(
            model_name='phoneuser',
            name='additional_calls',
            field=models.BooleanField(default=False, verbose_name=b'chiamate supplementari'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='phoneuser',
            name='language',
            field=models.CharField(default=b'it', max_length=4, verbose_name=b'lingua', choices=[(b'it', b'Italiano'), (b'en', b'Inglese'), (b'fr', b'Francese'), (b'de', b'Tedesco'), (b'es', b'Spagnolo'), (b'ar', b'Arabo')]),
        ),
    ]
