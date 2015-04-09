# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ArchivedRecord'
        db.create_table('archives_archivedrecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('archived_phoneuser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archives.ArchivedPhoneUser'])),
            ('calldate', self.gf('django.db.models.fields.DateTimeField')()),
            ('pincode', self.gf('django.db.models.fields.CharField')(default='', max_length=10)),
            ('uniqueid', self.gf('django.db.models.fields.CharField')(default='', max_length=32)),
            ('filename', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
        ))
        db.send_create_signal('archives', ['ArchivedRecord'])

        # Adding model 'ArchivedCredit'
        db.create_table('archives_archivedcredit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('archived_phoneuser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archives.ArchivedPhoneUser'])),
            ('recharge', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=5, decimal_places=2)),
            ('recharge_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('archives', ['ArchivedCredit'])

        # Adding model 'ArchivedWhitelist'
        db.create_table('archives_archivedwhitelist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('archived_phoneuser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archives.ArchivedPhoneUser'])),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('phonenumber', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('duration', self.gf('django.db.models.fields.IntegerField')()),
            ('frequency', self.gf('django.db.models.fields.IntegerField')()),
            ('extraordinary', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('real_mobile', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('archives', ['ArchivedWhitelist'])

        # Adding model 'ArchivedDetail'
        db.create_table('archives_archiveddetail', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('archived_phoneuser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archives.ArchivedPhoneUser'])),
            ('calldate', self.gf('django.db.models.fields.DateTimeField')()),
            ('clid', self.gf('django.db.models.fields.CharField')(default='', max_length=80)),
            ('src', self.gf('django.db.models.fields.CharField')(default='', max_length=80)),
            ('dst', self.gf('django.db.models.fields.CharField')(default='', max_length=80)),
            ('dcontext', self.gf('django.db.models.fields.CharField')(default='', max_length=80)),
            ('channel', self.gf('django.db.models.fields.CharField')(default='', max_length=80)),
            ('dstchannel', self.gf('django.db.models.fields.CharField')(default='', max_length=80)),
            ('lastapp', self.gf('django.db.models.fields.CharField')(default='', max_length=80)),
            ('lastdata', self.gf('django.db.models.fields.CharField')(default='', max_length=80)),
            ('duration', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('billsec', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('disposition', self.gf('django.db.models.fields.CharField')(default='', max_length=45)),
            ('amaflags', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('accountcode', self.gf('django.db.models.fields.CharField')(default='', max_length=20)),
            ('userfield', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('uniqueid', self.gf('django.db.models.fields.CharField')(default='', max_length=32)),
            ('linkedid', self.gf('django.db.models.fields.CharField')(default='', max_length=32)),
            ('sequence', self.gf('django.db.models.fields.CharField')(default='', max_length=32)),
            ('peeraccount', self.gf('django.db.models.fields.CharField')(default='', max_length=32)),
            ('price', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=7, decimal_places=4)),
            ('custom_src', self.gf('django.db.models.fields.CharField')(default='', max_length=80)),
            ('custom_dst', self.gf('django.db.models.fields.CharField')(default='', max_length=80)),
            ('custom_calltype', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('archives', ['ArchivedDetail'])

        # Adding model 'ArchivedPhoneUser'
        db.create_table('archives_archivedphoneuser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('pincode', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('serial_no', self.gf('django.db.models.fields.CharField')(default='', max_length=24)),
            ('listening_enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('recording_enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('vipaccount', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('four_bis_limited', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('archived_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('archives', ['ArchivedPhoneUser'])


    def backwards(self, orm):
        # Deleting model 'ArchivedRecord'
        db.delete_table('archives_archivedrecord')

        # Deleting model 'ArchivedCredit'
        db.delete_table('archives_archivedcredit')

        # Deleting model 'ArchivedWhitelist'
        db.delete_table('archives_archivedwhitelist')

        # Deleting model 'ArchivedDetail'
        db.delete_table('archives_archiveddetail')

        # Deleting model 'ArchivedPhoneUser'
        db.delete_table('archives_archivedphoneuser')


    models = {
        'archives.archivedcredit': {
            'Meta': {'object_name': 'ArchivedCredit'},
            'archived_phoneuser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archives.ArchivedPhoneUser']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recharge': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2'}),
            'recharge_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        'archives.archiveddetail': {
            'Meta': {'object_name': 'ArchivedDetail'},
            'accountcode': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'amaflags': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'archived_phoneuser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archives.ArchivedPhoneUser']"}),
            'billsec': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'calldate': ('django.db.models.fields.DateTimeField', [], {}),
            'channel': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'clid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'custom_calltype': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'custom_dst': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'custom_src': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'dcontext': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'disposition': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '45'}),
            'dst': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'dstchannel': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastapp': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'lastdata': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'linkedid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'}),
            'peeraccount': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '7', 'decimal_places': '4'}),
            'sequence': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'}),
            'src': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'uniqueid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'}),
            'userfield': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'archives.archivedphoneuser': {
            'Meta': {'object_name': 'ArchivedPhoneUser'},
            'archived_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'four_bis_limited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'listening_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pincode': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'recording_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'serial_no': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '24'}),
            'vipaccount': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'archives.archivedrecord': {
            'Meta': {'object_name': 'ArchivedRecord'},
            'archived_phoneuser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archives.ArchivedPhoneUser']"}),
            'calldate': ('django.db.models.fields.DateTimeField', [], {}),
            'filename': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pincode': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'}),
            'uniqueid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'})
        },
        'archives.archivedwhitelist': {
            'Meta': {'object_name': 'ArchivedWhitelist'},
            'archived_phoneuser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archives.ArchivedPhoneUser']"}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'extraordinary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'frequency': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phonenumber': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'real_mobile': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['archives']