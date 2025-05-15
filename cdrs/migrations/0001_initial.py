# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SuperbaCDR',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('calldate', models.DateTimeField()),
                ('src', models.CharField(default=b'', max_length=80)),
                ('dst', models.CharField(default=b'', max_length=80)),
                ('pincode', models.CharField(default=b'', max_length=40)),
                ('calltype', models.IntegerField(default=0, choices=[(0, b'ordinaria'), (1, b'strordinaria'), (2, b'speciale')])),
                ('direction', models.IntegerField(default=1, choices=[(0, b'interna'), (1, b'uscente'), (2, b'entrante')])),
                ('duration', models.IntegerField(default=0)),
                ('billsec', models.IntegerField(default=0)),
                ('price', models.DecimalField(default=0, max_digits=7, decimal_places=4)),
                ('valid', models.BooleanField(default=True)),
                ('uniqueid', models.CharField(default=b'', max_length=32)),
            ],
            options={
                'db_table': 'superbacdr',
            },
            bases=(models.Model,),
        ),
    ]
