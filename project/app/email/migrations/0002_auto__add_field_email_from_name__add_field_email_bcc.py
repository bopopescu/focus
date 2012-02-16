# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Email.from_name'
        db.add_column('email_email', 'from_name', self.gf('django.db.models.fields.CharField')(default='', max_length=230), keep_default=False)

        # Adding field 'Email.bcc'
        db.add_column('email_email', 'bcc', self.gf('django.db.models.fields.TextField')(default=''), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Email.from_name'
        db.delete_column('email_email', 'from_name')

        # Deleting field 'Email.bcc'
        db.delete_column('email_email', 'bcc')


    models = {
        'email.email': {
            'Meta': {'object_name': 'Email'},
            'bcc': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'cc': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'from_email': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'from_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '230'}),
            'html_body': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mailbox_hash': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'message_id': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'reply_to': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'subject': ('django.db.models.fields.TextField', [], {}),
            'tag': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'text_body': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'to': ('django.db.models.fields.TextField', [], {'default': "''"})
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
