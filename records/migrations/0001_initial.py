# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('calldate', models.DateTimeField(verbose_name=datetime.datetime(2016, 5, 4, 16, 34, 34, 225089))),
                ('pincode', models.CharField(default=b'', max_length=10)),
                ('uniqueid', models.CharField(default=b'', max_length=32)),
                ('filename', models.CharField(default=b'', max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
