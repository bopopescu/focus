# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Company'
        db.create_table('core_company', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
        ))
        db.send_create_signal('core', ['Company'])

        # Adding model 'Membership'
        db.create_table('core_membership', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='memberships', null=True, to=orm['core.Company'])),
        ))
        db.send_create_signal('core', ['Membership'])

        # Adding M2M table for field users on 'Membership'
        db.create_table('core_membership_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('membership', models.ForeignKey(orm['core.membership'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('core_membership_users', ['membership_id', 'user_id'])

        # Adding model 'ObjectPermission'
        db.create_table('core_objectpermission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='permissions', null=True, to=orm['auth.User'])),
            ('membership', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='permissions', null=True, to=orm['core.Membership'])),
            ('globalPermission', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('can_view', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('can_change', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('can_delete', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('negative', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('core', ['ObjectPermission'])

        # Adding model 'UserProfile'
        db.create_table('core_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='core_userprofile_users', null=True, to=orm['core.Company'])),
        ))
        db.send_create_signal('core', ['UserProfile'])


    def backwards(self, orm):
        
        # Deleting model 'Company'
        db.delete_table('core_company')

        # Deleting model 'Membership'
        db.delete_table('core_membership')

        # Removing M2M table for field users on 'Membership'
        db.delete_table('core_membership_users')

        # Deleting model 'ObjectPermission'
        db.delete_table('core_objectpermission')

        # Deleting model 'UserProfile'
        db.delete_table('core_userprofile')


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
        },
        'core.membership': {
            'Meta': {'object_name': 'Membership'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'memberships'", 'null': 'True', 'to': "orm['core.Company']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'memberships'", 'symmetrical': 'False', 'to': "orm['auth.User']"})
        },
        'core.objectpermission': {
            'Meta': {'object_name': 'ObjectPermission'},
            'can_change': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_delete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_view': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'globalPermission': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'membership': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'permissions'", 'null': 'True', 'to': "orm['core.Membership']"}),
            'negative': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'permissions'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'core.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'core_userprofile_users'", 'null': 'True', 'to': "orm['core.Company']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['core']
