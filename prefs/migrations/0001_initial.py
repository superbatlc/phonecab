# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fare',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('direction', models.CharField(max_length=80, verbose_name=b'Direttrice')),
                ('prefix_list', models.TextField(verbose_name=b'Lista prefissi')),
                ('connection_charge', models.FloatField(verbose_name=b'Scatto alla risposta')),
                ('fee_per_second', models.FloatField(verbose_name=b'Tariffa al secondo')),
                ('reg_exp', models.TextField(verbose_name=b'Espressione regolare')),
                ('ordering', models.IntegerField(verbose_name=b'Ordinamento')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pref',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=40)),
                ('value', models.CharField(max_length=40)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
