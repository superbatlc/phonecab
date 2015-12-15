# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recharge', models.DecimalField(default=0, verbose_name=b'ricarica', max_digits=5, decimal_places=2)),
                ('recharge_date', models.DateTimeField(default=datetime.datetime.now)),
                ('reason', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PhoneUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=35, verbose_name=b'nome')),
                ('last_name', models.CharField(max_length=50, verbose_name=b'cognome')),
                ('pincode', models.CharField(max_length=10, verbose_name=b'pin')),
                ('serial_no', models.CharField(default=b'', max_length=24, verbose_name=b'matricola')),
                ('listening_enabled', models.BooleanField(default=False, verbose_name=b'ascolto')),
                ('recording_enabled', models.BooleanField(default=False, verbose_name=b'registrazione')),
                ('enabled', models.BooleanField(default=True, verbose_name=b'stato')),
                ('balance', models.DecimalField(default=0, verbose_name=b'credito residuo', max_digits=7, decimal_places=4)),
                ('language', models.CharField(default=b'it', max_length=4, verbose_name=b'lingua', choices=[(b'it', b'Italiano'), (b'en', b'Inglese'), (b'fr', b'Francese'), (b'de', b'Tedesco'), (b'es', b'Spagnolo')])),
                ('vipaccount', models.BooleanField(default=False, verbose_name=b'senza restizioni')),
                ('four_bis_limited', models.BooleanField(default=False, verbose_name=b'4bis limitato')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Whitelist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=255, verbose_name=b'etichetta')),
                ('phonenumber', models.CharField(max_length=40, verbose_name=b'telefono')),
                ('duration', models.IntegerField(default=10, verbose_name=b'durata massima')),
                ('frequency', models.IntegerField(default=0, verbose_name=b'frequenza', choices=[(0, b'Primo Ingresso'), (1, b'Avvocato'), (2, b'Ordinaria'), (3, b'Ordinaria 4bis limitato')])),
                ('extraordinary', models.BooleanField(default=False, verbose_name=b'straordinaria')),
                ('real_mobile', models.BooleanField(default=False, verbose_name=b'cellulare')),
                ('enabled', models.BooleanField(default=False, verbose_name=b'stato')),
                ('phoneuser', models.ForeignKey(to='phoneusers.PhoneUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='credit',
            name='phoneuser',
            field=models.ForeignKey(to='phoneusers.PhoneUser'),
            preserve_default=True,
        ),
    ]
