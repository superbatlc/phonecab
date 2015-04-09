# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Record'
        db.create_table('records_record', (
            ('id', self.gf('django.db.models.fields.AutoField')
             (primary_key=True)),
            ('recorddate', self.gf('django.db.models.fields.DateTimeField')()),
            ('pincode', self.gf('django.db.models.fields.CharField')
             (default='', max_length=10)),
            ('uniqueid', self.gf('django.db.models.fields.CharField')
             (default='', max_length=32)),
            ('path', self.gf('django.db.models.fields.CharField')
             (default='', max_length=255)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')
             (default=False)),
        ))
        db.send_create_signal('records', ['Record'])

    def backwards(self, orm):
        # Deleting model 'Record'
        db.delete_table('records_record')

    models = {
        'records.record': {
            'Meta': {
                'object_name': 'Record'}, 'deleted': (
                'django.db.models.fields.BooleanField', [], {
                    'default': 'False'}), 'id': (
                        'django.db.models.fields.AutoField', [], {
                            'primary_key': 'True'}), 'path': (
                                'django.db.models.fields.CharField', [], {
                                    'default': "''", 'max_length': '255'}), 'pincode': (
                                        'django.db.models.fields.CharField', [], {
                                            'default': "''", 'max_length': '10'}), 'recorddate': (
                                                'django.db.models.fields.DateTimeField', [], {}), 'uniqueid': (
                                                    'django.db.models.fields.CharField', [], {
                                                        'default': "''", 'max_length': '32'})}}

    complete_apps = ['records']
