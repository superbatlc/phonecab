# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Pref'
        db.create_table('prefs_pref', (
            ('id', self.gf('django.db.models.fields.AutoField')
             (primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')
             (max_length=40)),
            ('value', self.gf('django.db.models.fields.CharField')
             (max_length=40)),
        ))
        db.send_create_signal('prefs', ['Pref'])

        # Adding model 'Fare'
        db.create_table('prefs_fare', (
            ('id', self.gf('django.db.models.fields.AutoField')
             (primary_key=True)),
            ('direction', self.gf(
                'django.db.models.fields.CharField')(max_length=80)),
            ('prefix_list', self.gf('django.db.models.fields.TextField')()),
            ('connection_charge', self.gf(
                'django.db.models.fields.FloatField')()),
            ('fee_per_second', self.gf(
                'django.db.models.fields.FloatField')()),
            ('reg_exp', self.gf('django.db.models.fields.TextField')()),
            ('ordering', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('prefs', ['Fare'])

    def backwards(self, orm):
        # Deleting model 'Pref'
        db.delete_table('prefs_pref')

        # Deleting model 'Fare'
        db.delete_table('prefs_fare')

    models = {
        'prefs.fare': {
            'Meta': {
                'object_name': 'Fare'}, 'connection_charge': (
                'django.db.models.fields.FloatField', [], {}), 'direction': (
                    'django.db.models.fields.CharField', [], {
                        'max_length': '80'}), 'fee_per_second': (
                            'django.db.models.fields.FloatField', [], {}), 'id': (
                                'django.db.models.fields.AutoField', [], {
                                    'primary_key': 'True'}), 'ordering': (
                                        'django.db.models.fields.IntegerField', [], {}), 'prefix_list': (
                                            'django.db.models.fields.TextField', [], {}), 'reg_exp': (
                                                'django.db.models.fields.TextField', [], {})}, 'prefs.pref': {
                                                    'Meta': {
                                                        'object_name': 'Pref'}, 'id': (
                                                            'django.db.models.fields.AutoField', [], {
                                                                'primary_key': 'True'}), 'key': (
                                                                    'django.db.models.fields.CharField', [], {
                                                                        'max_length': '40'}), 'value': (
                                                                            'django.db.models.fields.CharField', [], {
                                                                                'max_length': '40'})}}

    complete_apps = ['prefs']
