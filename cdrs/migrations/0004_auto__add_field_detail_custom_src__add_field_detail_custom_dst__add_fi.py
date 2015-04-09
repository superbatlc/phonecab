# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Detail.custom_src'
        db.add_column('cdrs_detail', 'custom_src',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=80),
                      keep_default=False)

        # Adding field 'Detail.custom_dst'
        db.add_column('cdrs_detail', 'custom_dst',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=80),
                      keep_default=False)

        # Adding field 'Detail.custom_calltype'
        db.add_column('cdrs_detail', 'custom_calltype',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Detail.deleted'
        db.add_column('cdrs_detail', 'deleted',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Detail.custom_src'
        db.delete_column('cdrs_detail', 'custom_src')

        # Deleting field 'Detail.custom_dst'
        db.delete_column('cdrs_detail', 'custom_dst')

        # Deleting field 'Detail.custom_calltype'
        db.delete_column('cdrs_detail', 'custom_calltype')

        # Deleting field 'Detail.deleted'
        db.delete_column('cdrs_detail', 'deleted')


    models = {
        'cdrs.detail': {
            'Meta': {'object_name': 'Detail'},
            'accountcode': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'amaflags': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'billsec': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'calldate': ('django.db.models.fields.DateTimeField', [], {}),
            'channel': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'clid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'custom_calltype': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'custom_dst': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'custom_src': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'dcontext': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'deleted': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'disposition': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '45'}),
            'dst': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'dstchannel': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastapp': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'lastdata': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'linkedid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'}),
            'peeraccount': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '-1.0', 'max_digits': '5', 'decimal_places': '2'}),
            'sequence': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'}),
            'src': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'uniqueid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'}),
            'userfield': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'cdrs.realtimecall': {
            'Meta': {'object_name': 'RealTimeCall'},
            'balance': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'calldate': ('django.db.models.fields.IntegerField', [], {}),
            'channel': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'connection_charge': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'dst': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'fee_per_second': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_duration': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pincode': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'}),
            'src': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'})
        }
    }

    complete_apps = ['cdrs']