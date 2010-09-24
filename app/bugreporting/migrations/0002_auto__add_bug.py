# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Bug'
        db.create_table('bugreporting_bug', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_edited', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('bugreporting', ['Bug'])


    def backwards(self, orm):
        
        # Deleting model 'Bug'
        db.delete_table('bugreporting_bug')


    models = {
        'bugreporting.bug': {
            'Meta': {'object_name': 'Bug'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        }
    }

    complete_apps = ['bugreporting']
