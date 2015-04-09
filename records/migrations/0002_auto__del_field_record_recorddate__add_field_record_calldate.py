# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Record.recorddate'
        db.delete_column('records_record', 'recorddate')

        # Adding field 'Record.calldate'
        db.add_column('records_record', 'calldate',
                      self.gf('django.db.models.fields.DateTimeField')(
                          default=datetime.datetime(2014, 7, 14, 0, 0)),
                      keep_default=False)

    def backwards(self, orm):
        # Adding field 'Record.recorddate'
        db.add_column('records_record', 'recorddate',
                      self.gf('django.db.models.fields.DateTimeField')(
                          default='0000-00-00 00:00:00'),
                      keep_default=False)

        # Deleting field 'Record.calldate'
        db.delete_column('records_record', 'calldate')

    models = {
        'records.record': {
            'Meta': {
                'object_name': 'Record'}, 'calldate': (
                'django.db.models.fields.DateTimeField', [], {}), 'deleted': (
                    'django.db.models.fields.BooleanField', [], {
                        'default': 'False'}), 'id': (
                            'django.db.models.fields.AutoField', [], {
                                'primary_key': 'True'}), 'path': (
                                    'django.db.models.fields.CharField', [], {
                                        'default': "''", 'max_length': '255'}), 'pincode': (
                                            'django.db.models.fields.CharField', [], {
                                                'default': "''", 'max_length': '10'}), 'uniqueid': (
                                                    'django.db.models.fields.CharField', [], {
                                                        'default': "''", 'max_length': '32'})}}

    complete_apps = ['records']
