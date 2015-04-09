# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Record.path'
        db.delete_column('records_record', 'path')

        # Adding field 'Record.filename'
        db.add_column('records_record', 'filename',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Record.path'
        db.add_column('records_record', 'path',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Deleting field 'Record.filename'
        db.delete_column('records_record', 'filename')


    models = {
        'records.record': {
            'Meta': {'object_name': 'Record'},
            'calldate': ('django.db.models.fields.DateTimeField', [], {}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'filename': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pincode': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'}),
            'uniqueid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'})
        }
    }

    complete_apps = ['records']