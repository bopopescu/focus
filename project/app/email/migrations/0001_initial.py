# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Email'
        db.create_table('email_email', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_email', self.gf('django.db.models.fields.TextField')()),
            ('to', self.gf('django.db.models.fields.TextField')()),
            ('cc', self.gf('django.db.models.fields.TextField')()),
            ('subject', self.gf('django.db.models.fields.TextField')()),
            ('message_id', self.gf('django.db.models.fields.TextField')()),
            ('tag', self.gf('django.db.models.fields.TextField')()),
            ('reply_to', self.gf('django.db.models.fields.TextField')()),
            ('mailbox_hash', self.gf('django.db.models.fields.TextField')()),
            ('text_body', self.gf('django.db.models.fields.TextField')()),
            ('html_body', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('email', ['Email'])

        # Adding model 'EmailHeader'
        db.create_table('email_emailheader', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.related.ForeignKey')(related_name='headers', to=orm['email.Email'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=230)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=230)),
        ))
        db.send_create_signal('email', ['EmailHeader'])

        # Adding model 'EmailAttachment'
        db.create_table('email_emailattachment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.related.ForeignKey')(related_name='attachments', to=orm['email.Email'])),
            ('content_length', self.gf('django.db.models.fields.CharField')(max_length=230)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=230)),
            ('content_type', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('email', ['EmailAttachment'])


    def backwards(self, orm):
        
        # Deleting model 'Email'
        db.delete_table('email_email')

        # Deleting model 'EmailHeader'
        db.delete_table('email_emailheader')

        # Deleting model 'EmailAttachment'
        db.delete_table('email_emailattachment')


    models = {
        'email.email': {
            'Meta': {'object_name': 'Email'},
            'cc': ('django.db.models.fields.TextField', [], {}),
            'from_email': ('django.db.models.fields.TextField', [], {}),
            'html_body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mailbox_hash': ('django.db.models.fields.TextField', [], {}),
            'message_id': ('django.db.models.fields.TextField', [], {}),
            'reply_to': ('django.db.models.fields.TextField', [], {}),
            'subject': ('django.db.models.fields.TextField', [], {}),
            'tag': ('django.db.models.fields.TextField', [], {}),
            'text_body': ('django.db.models.fields.TextField', [], {}),
            'to': ('django.db.models.fields.TextField', [], {})
        },
        'email.emailattachment': {
            'Meta': {'object_name': 'EmailAttachment'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'content_length': ('django.db.models.fields.CharField', [], {'max_length': '230'}),
            'content_type': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'email': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attachments'", 'to': "orm['email.Email']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '230'})
        },
        'email.emailheader': {
            'Meta': {'object_name': 'EmailHeader'},
            'email': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'headers'", 'to': "orm['email.Email']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '230'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '230'})
        }
    }

    complete_apps = ['email']
