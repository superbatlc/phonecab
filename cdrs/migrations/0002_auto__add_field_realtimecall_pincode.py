# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'RealTimeCall.pincode'
        db.add_column('cdrs_realtimecall', 'pincode',
                      self.gf('django.db.models.fields.CharField')(
                          default='', max_length=10),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'RealTimeCall.pincode'
        db.delete_column('cdrs_realtimecall', 'pincode')

    models = {
        'cdrs.detail': {
            'Meta': {
                'object_name': 'Detail'}, 'accountcode': (
                'django.db.models.fields.CharField', [], {
                    'default': "''", 'max_length': '20'}), 'amaflags': (
                        'django.db.models.fields.IntegerField', [], {
                            'default': '0'}), 'billsec': (
                                'django.db.models.fields.IntegerField', [], {
                                    'default': '0'}), 'calldate': (
                                        'django.db.models.fields.DateTimeField', [], {}), 'channel': (
                                            'django.db.models.fields.CharField', [], {
                                                'default': "''", 'max_length': '80'}), 'clid': (
                                                    'django.db.models.fields.CharField', [], {
                                                        'default': "''", 'max_length': '80'}), 'dcontext': (
                                                            'django.db.models.fields.CharField', [], {
                                                                'default': "''", 'max_length': '80'}), 'disposition': (
                                                                    'django.db.models.fields.CharField', [], {
                                                                        'default': "''", 'max_length': '45'}), 'dst': (
                                                                            'django.db.models.fields.CharField', [], {
                                                                                'default': "''", 'max_length': '80'}), 'dstchannel': (
                                                                                    'django.db.models.fields.CharField', [], {
                                                                                        'default': "''", 'max_length': '80'}), 'duration': (
                                                                                            'django.db.models.fields.IntegerField', [], {
                                                                                                'default': '0'}), 'id': (
                                                                                                    'django.db.models.fields.AutoField', [], {
                                                                                                        'primary_key': 'True'}), 'lastapp': (
                                                                                                            'django.db.models.fields.CharField', [], {
                                                                                                                'default': "''", 'max_length': '80'}), 'lastdata': (
                                                                                                                    'django.db.models.fields.CharField', [], {
                                                                                                                        'default': "''", 'max_length': '80'}), 'linkedid': (
                                                                                                                            'django.db.models.fields.CharField', [], {
                                                                                                                                'default': "''", 'max_length': '32'}), 'peeraccount': (
                                                                                                                                    'django.db.models.fields.CharField', [], {
                                                                                                                                        'default': "''", 'max_length': '32'}), 'price': (
                                                                                                                                            'django.db.models.fields.FloatField', [], {
                                                                                                                                                'default': "'-1.00'"}), 'sequence': (
                                                                                                                                                    'django.db.models.fields.CharField', [], {
                                                                                                                                                        'default': "''", 'max_length': '32'}), 'src': (
                                                                                                                                                            'django.db.models.fields.CharField', [], {
                                                                                                                                                                'default': "''", 'max_length': '80'}), 'uniqueid': (
                                                                                                                                                                    'django.db.models.fields.CharField', [], {
                                                                                                                                                                        'default': "''", 'max_length': '32'}), 'userfield': (
                                                                                                                                                                            'django.db.models.fields.CharField', [], {
                                                                                                                                                                                'default': "''", 'max_length': '255'})}, 'cdrs.realtimecall': {
                                                                                                                                                                                    'Meta': {
                                                                                                                                                                                        'object_name': 'RealTimeCall'}, 'balance': (
                                                                                                                                                                                            'django.db.models.fields.FloatField', [], {
                                                                                                                                                                                                'default': '0'}), 'calldate': (
                                                                                                                                                                                                    'django.db.models.fields.IntegerField', [], {}), 'channel': (
                                                                                                                                                                                                        'django.db.models.fields.CharField', [], {
                                                                                                                                                                                                            'default': "''", 'max_length': '80'}), 'connection_charge': (
                                                                                                                                                                                                                'django.db.models.fields.FloatField', [], {
                                                                                                                                                                                                                    'default': '0'}), 'dst': (
                                                                                                                                                                                                                        'django.db.models.fields.CharField', [], {
                                                                                                                                                                                                                            'default': "''", 'max_length': '80'}), 'fee_per_second': (
                                                                                                                                                                                                                                'django.db.models.fields.FloatField', [], {
                                                                                                                                                                                                                                    'default': '0'}), 'id': (
                                                                                                                                                                                                                                        'django.db.models.fields.AutoField', [], {
                                                                                                                                                                                                                                            'primary_key': 'True'}), 'max_duration': (
                                                                                                                                                                                                                                                'django.db.models.fields.IntegerField', [], {
                                                                                                                                                                                                                                                    'default': '0'}), 'pincode': (
                                                                                                                                                                                                                                                        'django.db.models.fields.CharField', [], {
                                                                                                                                                                                                                                                            'default': "''", 'max_length': '10'}), 'src': (
                                                                                                                                                                                                                                                                'django.db.models.fields.CharField', [], {
                                                                                                                                                                                                                                                                    'default': "''", 'max_length': '80'})}}

    complete_apps = ['cdrs']
