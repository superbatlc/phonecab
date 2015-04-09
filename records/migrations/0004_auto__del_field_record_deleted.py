# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Record.deleted'
        db.delete_column('records_record', 'deleted')


    def backwards(self, orm):
        # Adding field 'Record.deleted'
        db.add_column('records_record', 'deleted',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    models = {
        'records.record': {
            'Meta': {'object_name': 'Record'},
            'calldate': ('django.db.models.fields.DateTimeField', [], {}),
            'filename': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pincode': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'}),
            'uniqueid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'})
        }
    }

    complete_apps = ['records']