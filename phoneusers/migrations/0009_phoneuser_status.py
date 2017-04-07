# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phoneusers', '0008_whitelist_additional'),
    ]

    operations = [
        migrations.AddField(
            model_name='phoneuser',
            name='status',
            field=models.IntegerField(default=0, verbose_name=b'stato', choices=[(0, b'nuovo arrivo'), (1, b'in attesa di giudizio'), (2, b'definitivo')]),
        ),
    ]
