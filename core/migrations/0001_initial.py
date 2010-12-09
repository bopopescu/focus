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

        # Adding model 'AnonymousUser'
        db.create_table('core_anonymoususer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('core', ['AnonymousUser'])

        # Adding model 'User'
        db.create_table('core_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='core_user_users', null=True, to=orm['core.Company'])),
            ('canLogin', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('profileImage', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('core', ['User'])

        # Adding model 'Notification'
        db.create_table('core_notification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notifications', to=orm['core.User'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('read', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notifications', null=True, to=orm['core.Company'])),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='createdNotifications', null=True, to=orm['core.User'])),
            ('sendEmail', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('core', ['Notification'])

        # Adding model 'Log'
        db.create_table('core_log', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='logs', null=True, to=orm['core.User'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(related_name='logs', null=True, to=orm['core.Company'])),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
        ))
        db.send_create_signal('core', ['Log'])

        # Adding model 'Membership'
        db.create_table('core_membership', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2010, 12, 9, 2, 0, 21, 74012))),
            ('date_edited', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2010, 12, 9, 2, 0, 21, 74049))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='membership_created', null=True, blank=True, to=orm['core.User'])),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='membership_edited', null=True, blank=True, to=orm['core.User'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='membership_edited', null=True, blank=True, to=orm['core.Company'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='children', null=True, to=orm['core.Membership'])),
        ))
        db.send_create_signal('core', ['Membership'])

        # Adding M2M table for field members on 'Membership'
        db.create_table('core_membership_members', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('membership', models.ForeignKey(orm['core.membership'], null=False)),
            ('user', models.ForeignKey(orm['core.user'], null=False))
        ))
        db.create_unique('core_membership_members', ['membership_id', 'user_id'])

        # Adding model 'Action'
        db.create_table('core_action', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('verb', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('core', ['Action'])

        # Adding model 'Role'
        db.create_table('core_role', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal('core', ['Role'])

        # Adding M2M table for field actions on 'Role'
        db.create_table('core_role_actions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('role', models.ForeignKey(orm['core.role'], null=False)),
            ('action', models.ForeignKey(orm['core.action'], null=False))
        ))
        db.create_unique('core_role_actions', ['role_id', 'action_id'])

        # Adding model 'Permission'
        db.create_table('core_permission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='permissions', null=True, to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='permissions', null=True, to=orm['core.User'])),
            ('membership', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='permissions', null=True, to=orm['core.Membership'])),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='permissions', null=True, to=orm['core.Role'])),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('core', ['Permission'])


    def backwards(self, orm):
        
        # Deleting model 'Company'
        db.delete_table('core_company')

        # Deleting model 'AnonymousUser'
        db.delete_table('core_anonymoususer')

        # Deleting model 'User'
        db.delete_table('core_user')

        # Deleting model 'Notification'
        db.delete_table('core_notification')

        # Deleting model 'Log'
        db.delete_table('core_log')

        # Deleting model 'Membership'
        db.delete_table('core_membership')

        # Removing M2M table for field members on 'Membership'
        db.delete_table('core_membership_members')

        # Deleting model 'Action'
        db.delete_table('core_action')

        # Deleting model 'Role'
        db.delete_table('core_role')

        # Removing M2M table for field actions on 'Role'
        db.delete_table('core_role_actions')

        # Deleting model 'Permission'
        db.delete_table('core_permission')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.action': {
            'Meta': {'object_name': 'Action'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'verb': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'core.anonymoususer': {
            'Meta': {'object_name': 'AnonymousUser'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'core.company': {
            'Meta': {'object_name': 'Company'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'core.log': {
            'Meta': {'object_name': 'Log'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'logs'", 'null': 'True', 'to': "orm['core.Company']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'logs'", 'null': 'True', 'to': "orm['core.User']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'})
        },
        'core.membership': {
            'Meta': {'object_name': 'Membership'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'membership_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'membership_created'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 12, 9, 2, 0, 21, 74012)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 12, 9, 2, 0, 21, 74049)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'membership_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'memberships'", 'symmetrical': 'False', 'to': "orm['core.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'null': 'True', 'to': "orm['core.Membership']"})
        },
        'core.notification': {
            'Meta': {'object_name': 'Notification'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notifications'", 'null': 'True', 'to': "orm['core.Company']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'createdNotifications'", 'null': 'True', 'to': "orm['core.User']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notifications'", 'to': "orm['core.User']"}),
            'sendEmail': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'core.permission': {
            'Meta': {'object_name': 'Permission'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'permissions'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'membership': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'permissions'", 'null': 'True', 'to': "orm['core.Membership']"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'permissions'", 'null': 'True', 'to': "orm['core.Role']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'permissions'", 'null': 'True', 'to': "orm['core.User']"})
        },
        'core.role': {
            'Meta': {'object_name': 'Role'},
            'actions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'role'", 'symmetrical': 'False', 'to': "orm['core.Action']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'core.user': {
            'Meta': {'object_name': 'User'},
            'canLogin': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'core_user_users'", 'null': 'True', 'to': "orm['core.Company']"}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'profileImage': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['core']
