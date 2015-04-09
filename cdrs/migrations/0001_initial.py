# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Detail'
        db.create_table('cdrs_detail', (
            ('id', self.gf('django.db.models.fields.AutoField')
             (primary_key=True)),
            ('calldate', self.gf('django.db.models.fields.DateTimeField')()),
            ('clid', self.gf('django.db.models.fields.CharField')
             (default='', max_length=80)),
            ('src', self.gf('django.db.models.fields.CharField')
             (default='', max_length=80)),
            ('dst', self.gf('django.db.models.fields.CharField')
             (default='', max_length=80)),
            ('dcontext', self.gf('django.db.models.fields.CharField')
             (default='', max_length=80)),
            ('channel', self.gf('django.db.models.fields.CharField')
             (default='', max_length=80)),
            ('dstchannel', self.gf('django.db.models.fields.CharField')
             (default='', max_length=80)),
            ('lastapp', self.gf('django.db.models.fields.CharField')
             (default='', max_length=80)),
            ('lastdata', self.gf('django.db.models.fields.CharField')
             (default='', max_length=80)),
            ('duration', self.gf(
                'django.db.models.fields.IntegerField')(default=0)),
            ('billsec', self.gf(
                'django.db.models.fields.IntegerField')(default=0)),
            ('disposition', self.gf('django.db.models.fields.CharField')
             (default='', max_length=45)),
            ('amaflags', self.gf(
                'django.db.models.fields.IntegerField')(default=0)),
            ('accountcode', self.gf('django.db.models.fields.CharField')
             (default='', max_length=20)),
            ('userfield', self.gf('django.db.models.fields.CharField')
             (default='', max_length=255)),
            ('uniqueid', self.gf('django.db.models.fields.CharField')
             (default='', max_length=32)),
            ('linkedid', self.gf('django.db.models.fields.CharField')
             (default='', max_length=32)),
            ('sequence', self.gf('django.db.models.fields.CharField')
             (default='', max_length=32)),
            ('peeraccount', self.gf('django.db.models.fields.CharField')
             (default='', max_length=32)),
            ('price', self.gf('django.db.models.fields.FloatField')
             (default='-1.00')),
        ))
        db.send_create_signal('cdrs', ['Detail'])

        # Adding model 'RealTimeCall'
        db.create_table('cdrs_realtimecall', (
            ('id', self.gf('django.db.models.fields.AutoField')
             (primary_key=True)),
            ('src', self.gf('django.db.models.fields.CharField')
             (default='', max_length=80)),
            ('dst', self.gf('django.db.models.fields.CharField')
             (default='', max_length=80)),
            ('calldate', self.gf('django.db.models.fields.IntegerField')()),
            ('max_duration', self.gf(
                'django.db.models.fields.IntegerField')(default=0)),
            ('balance', self.gf(
                'django.db.models.fields.FloatField')(default=0)),
            ('connection_charge', self.gf(
                'django.db.models.fields.FloatField')(default=0)),
            ('fee_per_second', self.gf(
                'django.db.models.fields.FloatField')(default=0)),
            ('channel', self.gf('django.db.models.fields.CharField')
             (default='', max_length=80)),
        ))
        db.send_create_signal('cdrs', ['RealTimeCall'])

    def backwards(self, orm):
        # Deleting model 'Detail'
        db.delete_table('cdrs_detail')

        # Deleting model 'RealTimeCall'
        db.delete_table('cdrs_realtimecall')

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
                                                                                                                                                                                                                                                    'default': '0'}), 'src': (
                                                                                                                                                                                                                                                        'django.db.models.fields.CharField', [], {
                                                                                                                                                                                                                                                            'default': "''", 'max_length': '80'})}}

    complete_apps = ['cdrs']
