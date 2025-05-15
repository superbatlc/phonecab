# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Acl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('function', models.CharField(max_length=1, choices=[(0, b'Anagrafica'), (1, b'Whitelist'), (2, b'Ricarica'), (3, b'Dettaglio'), (4, b'Registrazione')])),
                ('permission', models.CharField(max_length=1, choices=[(0, b'Nessuno'), (1, b'Lettura'), (3, b'Scrittura')])),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
