# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'BugComment.image'
        db.alter_column('bugreporting_bugcomment', 'image', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True))

        # Adding M2M table for field usersNotSeenChanges on 'Bug'
        db.create_table('bugreporting_bug_usersNotSeenChanges', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bug', models.ForeignKey(orm['bugreporting.bug'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('bugreporting_bug_usersNotSeenChanges', ['bug_id', 'user_id'])

        # Changing field 'Bug.image'
        db.alter_column('bugreporting_bug', 'image', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True))


    def backwards(self, orm):
        
        # Changing field 'BugComment.image'
        db.alter_column('bugreporting_bugcomment', 'image', self.gf('django.db.models.fields.files.FileField')(max_length=100))

        # Removing M2M table for field usersNotSeenChanges on 'Bug'
        db.delete_table('bugreporting_bug_usersNotSeenChanges')

        # Changing field 'Bug.image'
        db.alter_column('bugreporting_bug', 'image', self.gf('django.db.models.fields.files.FileField')(max_length=100))


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'bugreporting.bug': {
            'Meta': {'object_name': 'Bug'},
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'bug_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'bug_created'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 10, 8, 16, 59, 54, 892953)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 10, 8, 16, 59, 54, 893004)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'bug_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'usersNotSeenChanges': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'unseen_bugs_changes'", 'symmetrical': 'False', 'to': "orm['auth.User']"})
        },
        'bugreporting.bugcomment': {
            'Meta': {'object_name': 'BugComment'},
            'bug': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': "orm['bugreporting.Bug']"}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'bugcomment_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'bugcomment_created'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 10, 8, 16, 59, 54, 892953)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 10, 8, 16, 59, 54, 893004)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'bugcomment_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.company': {
            'Meta': {'object_name': 'Company'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        }
    }

    complete_apps = ['bugreporting']
