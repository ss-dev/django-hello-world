# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LogRequest'
        db.create_table('hello_logrequest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('hello', ['LogRequest'])


    def backwards(self, orm):
        # Deleting model 'LogRequest'
        db.delete_table('hello_logrequest')


    models = {
        'hello.contact': {
            'Meta': {'object_name': 'Contact'},
            'bio': ('django.db.models.fields.TextField', [], {}),
            'contacts': ('django.db.models.fields.TextField', [], {}),
            'date_birth': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jabber': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'hello.logrequest': {
            'Meta': {'object_name': 'LogRequest'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['hello']