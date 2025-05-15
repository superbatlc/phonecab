# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archives', '0005_auto_20151215_1351'),
    ]

    operations = [
        migrations.RenameField(
            model_name='archiveddetail',
            old_name='amaflags',
            new_name='calltype',
        ),
        migrations.RemoveField(
            model_name='archiveddetail',
            name='accountcode',
        ),
        migrations.RemoveField(
            model_name='archiveddetail',
            name='channel',
        ),
        migrations.RemoveField(
            model_name='archiveddetail',
            name='clid',
        ),
        migrations.RemoveField(
            model_name='archiveddetail',
            name='custom_calltype',
        ),
        migrations.RemoveField(
            model_name='archiveddetail',
            name='custom_dst',
        ),
        migrations.RemoveField(
            model_name='archiveddetail',
            name='custom_src',
        ),
        migrations.RemoveField(
            model_name='archiveddetail',
            name='custom_valid',
        ),
        migrations.RemoveField(
            model_name='archiveddetail',
            name='dcontext',
        ),
        migrations.RemoveField(
            model_name='archiveddetail',
            name='disposition',
        ),
        migrations.RemoveField(
            model_name='archiveddetail',
            name='dstchannel',
        ),
        migrations.RemoveField(
            model_name='archiveddetail',
            name='lastapp',
        ),
        migrations.RemoveField(
            model_name='archiveddetail',
            name='lastdata',
        ),
        migrations.RemoveField(
            model_name='archiveddetail',
            name='linkedid',
        ),
        migrations.RemoveField(
            model_name='archiveddetail',
            name='peeraccount',
        ),
        migrations.RemoveField(
            model_name='archiveddetail',
            name='sequence',
        ),
        migrations.RemoveField(
            model_name='archiveddetail',
            name='userfield',
        ),
        migrations.AddField(
            model_name='archiveddetail',
            name='direction',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='archiveddetail',
            name='pincode',
            field=models.CharField(default=b'', max_length=40),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='archiveddetail',
            name='valid',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
