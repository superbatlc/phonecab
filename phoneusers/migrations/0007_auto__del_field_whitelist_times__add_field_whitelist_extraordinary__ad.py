# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Whitelist.times'
        db.delete_column('phoneusers_whitelist', 'times')

        # Adding field 'Whitelist.extraordinary'
        db.add_column('phoneusers_whitelist', 'extraordinary',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Whitelist.real_mobile'
        db.add_column('phoneusers_whitelist', 'real_mobile',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Whitelist.times'
        db.add_column('phoneusers_whitelist', 'times',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'Whitelist.extraordinary'
        db.delete_column('phoneusers_whitelist', 'extraordinary')

        # Deleting field 'Whitelist.real_mobile'
        db.delete_column('phoneusers_whitelist', 'real_mobile')


    models = {
        'phoneusers.credit': {
            'Meta': {'object_name': 'Credit'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phoneuser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['phoneusers.PhoneUser']"}),
            'recharge': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2'}),
            'recharge_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'phoneusers.phoneuser': {
            'Meta': {'object_name': 'PhoneUser'},
            'balance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'it'", 'max_length': '4'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'listening_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pincode': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'recording_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'serial_no': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '24'}),
            'vipaccount': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'phoneusers.whitelist': {
            'Meta': {'object_name': 'Whitelist'},
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'extraordinary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'frequency': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phonenumber': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'phoneuser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['phoneusers.PhoneUser']"}),
            'real_mobile': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['phoneusers']