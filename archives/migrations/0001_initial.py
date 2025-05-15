# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArchivedCredit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recharge', models.DecimalField(default=0, verbose_name=b'ricarica', max_digits=5, decimal_places=2)),
                ('recharge_date', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArchivedDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('calldate', models.DateTimeField()),
                ('clid', models.CharField(default=b'', max_length=80)),
                ('src', models.CharField(default=b'', max_length=80)),
                ('dst', models.CharField(default=b'', max_length=80)),
                ('dcontext', models.CharField(default=b'', max_length=80)),
                ('channel', models.CharField(default=b'', max_length=80)),
                ('dstchannel', models.CharField(default=b'', max_length=80)),
                ('lastapp', models.CharField(default=b'', max_length=80)),
                ('lastdata', models.CharField(default=b'', max_length=80)),
                ('duration', models.IntegerField(default=0)),
                ('billsec', models.IntegerField(default=0)),
                ('disposition', models.CharField(default=b'', max_length=45)),
                ('amaflags', models.IntegerField(default=0)),
                ('accountcode', models.CharField(default=b'', max_length=20)),
                ('userfield', models.CharField(default=b'', max_length=255)),
                ('uniqueid', models.CharField(default=b'', max_length=32)),
                ('linkedid', models.CharField(default=b'', max_length=32)),
                ('sequence', models.CharField(default=b'', max_length=32)),
                ('peeraccount', models.CharField(default=b'', max_length=32)),
                ('price', models.DecimalField(default=0, max_digits=7, decimal_places=4)),
                ('custom_src', models.CharField(default=b'', max_length=80)),
                ('custom_dst', models.CharField(default=b'', max_length=80)),
                ('custom_calltype', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArchivedPhoneUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=35, verbose_name=b'nome')),
                ('last_name', models.CharField(max_length=50, verbose_name=b'cognome')),
                ('pincode', models.CharField(max_length=10, verbose_name=b'pin')),
                ('serial_no', models.CharField(default=b'', max_length=24, verbose_name=b'matricola')),
                ('listening_enabled', models.BooleanField(default=False, verbose_name=b'ascolto')),
                ('recording_enabled', models.BooleanField(default=False, verbose_name=b'registrazione')),
                ('language', models.CharField(max_length=4, verbose_name=b'lingua', choices=[(b'it', b'Italiano'), (b'en', b'Inglese'), (b'fr', b'Francese'), (b'de', b'Tedesco'), (b'es', b'Spagnolo'), (b'ar', b'Arabo')])),
                ('vipaccount', models.BooleanField(default=False, verbose_name=b'senza restizioni')),
                ('four_bis_limited', models.BooleanField(default=False, verbose_name=b'4bis limitato')),
                ('archived_date', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArchivedRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('calldate', models.DateTimeField()),
                ('pincode', models.CharField(default=b'', max_length=10)),
                ('uniqueid', models.CharField(default=b'', max_length=32)),
                ('filename', models.CharField(default=b'', max_length=255)),
                ('archived_phoneuser', models.ForeignKey(to='archives.ArchivedPhoneUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArchivedWhitelist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=255, verbose_name=b'etichetta')),
                ('phonenumber', models.CharField(max_length=40, verbose_name=b'telefono')),
                ('duration', models.IntegerField(verbose_name=b'durata massima')),
                ('frequency', models.IntegerField(verbose_name=b'frequenza', choices=[(0, b'Primo Ingresso'), (1, b'Avvocato'), (2, b'Ordinaria'), (3, b'Ordinaria 4bis limitato')])),
                ('extraordinary', models.BooleanField(default=False, verbose_name=b'straordinaria')),
                ('real_mobile', models.BooleanField(default=False, verbose_name=b'cellulare')),
                ('archived_phoneuser', models.ForeignKey(to='archives.ArchivedPhoneUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='archiveddetail',
            name='archived_phoneuser',
            field=models.ForeignKey(to='archives.ArchivedPhoneUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='archivedcredit',
            name='archived_phoneuser',
            field=models.ForeignKey(to='archives.ArchivedPhoneUser'),
            preserve_default=True,
        ),
    ]
