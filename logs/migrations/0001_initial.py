# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('when', models.DateTimeField()),
                ('what', models.TextField()),
                ('level', models.IntegerField(default=0, choices=[(0, b'info'), (1, b'warning'), (2, b'error')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
