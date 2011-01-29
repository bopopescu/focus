# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Company.daysIntoNextMonthTypeOfHourRegistration'
        db.delete_column('core_company', 'daysIntoNextMonthTypeOfHourRegistration')

        # Adding field 'Company.daysIntoNextMonthHourRegistration'
        db.add_column('core_company', 'daysIntoNextMonthHourRegistration', self.gf('django.db.models.fields.IntegerField')(default=3), keep_default=False)

        # Changing field 'Permission.deleted'
        db.alter_column('core_permission', 'deleted', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Permission.negative'
        db.alter_column('core_permission', 'negative', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Notification.sendEmail'
        db.alter_column('core_notification', 'sendEmail', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Notification.read'
        db.alter_column('core_notification', 'read', self.gf('django.db.models.fields.BooleanField')())

        # Deleting field 'User.daysIntoNextMonthTypeOfHourRegistrationExpire'
        db.delete_column('core_user', 'daysIntoNextMonthTypeOfHourRegistrationExpire')

        # Deleting field 'User.daysIntoNextMonthTypeOfHourRegistration'
        db.delete_column('core_user', 'daysIntoNextMonthTypeOfHourRegistration')

        # Deleting field 'User.validEditBackToDate'
        db.delete_column('core_user', 'validEditBackToDate')

        # Deleting field 'User.validEditBackToDateExpire'
        db.delete_column('core_user', 'validEditBackToDateExpire')

        # Adding field 'User.validEditHourRegistrationsToDate'
        db.add_column('core_user', 'validEditHourRegistrationsToDate', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)

        # Adding field 'User.validEditHourRegistrationsFromDate'
        db.add_column('core_user', 'validEditHourRegistrationsFromDate', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)

        # Adding field 'User.validEditHourRegistrationsExpireDate'
        db.add_column('core_user', 'validEditHourRegistrationsExpireDate', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)

        # Changing field 'User.deleted'
        db.alter_column('core_user', 'deleted', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'User.is_active'
        db.alter_column('core_user', 'is_active', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'User.is_superuser'
        db.alter_column('core_user', 'is_superuser', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'User.is_staff'
        db.alter_column('core_user', 'is_staff', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'User.canLogin'
        db.alter_column('core_user', 'canLogin', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Group.deleted'
        db.alter_column('core_group', 'deleted', self.gf('django.db.models.fields.BooleanField')())


    def backwards(self, orm):
        
        # Adding field 'Company.daysIntoNextMonthTypeOfHourRegistration'
        db.add_column('core_company', 'daysIntoNextMonthTypeOfHourRegistration', self.gf('django.db.models.fields.IntegerField')(default=3), keep_default=False)

        # Deleting field 'Company.daysIntoNextMonthHourRegistration'
        db.delete_column('core_company', 'daysIntoNextMonthHourRegistration')

        # Changing field 'Permission.deleted'
        db.alter_column('core_permission', 'deleted', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'Permission.negative'
        db.alter_column('core_permission', 'negative', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'Notification.sendEmail'
        db.alter_column('core_notification', 'sendEmail', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'Notification.read'
        db.alter_column('core_notification', 'read', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Adding field 'User.daysIntoNextMonthTypeOfHourRegistrationExpire'
        db.add_column('core_user', 'daysIntoNextMonthTypeOfHourRegistrationExpire', self.gf('django.db.models.fields.DateField')(null=True), keep_default=False)

        # Adding field 'User.daysIntoNextMonthTypeOfHourRegistration'
        db.add_column('core_user', 'daysIntoNextMonthTypeOfHourRegistration', self.gf('django.db.models.fields.IntegerField')(null=True), keep_default=False)

        # Adding field 'User.validEditBackToDate'
        db.add_column('core_user', 'validEditBackToDate', self.gf('django.db.models.fields.DateField')(null=True), keep_default=False)

        # Adding field 'User.validEditBackToDateExpire'
        db.add_column('core_user', 'validEditBackToDateExpire', self.gf('django.db.models.fields.DateField')(null=True), keep_default=False)

        # Deleting field 'User.validEditHourRegistrationsToDate'
        db.delete_column('core_user', 'validEditHourRegistrationsToDate')

        # Deleting field 'User.validEditHourRegistrationsFromDate'
        db.delete_column('core_user', 'validEditHourRegistrationsFromDate')

        # Deleting field 'User.validEditHourRegistrationsExpireDate'
        db.delete_column('core_user', 'validEditHourRegistrationsExpireDate')

        # Changing field 'User.deleted'
        db.alter_column('core_user', 'deleted', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'User.is_active'
        db.alter_column('core_user', 'is_active', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'User.is_superuser'
        db.alter_column('core_user', 'is_superuser', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'User.is_staff'
        db.alter_column('core_user', 'is_staff', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'User.canLogin'
        db.alter_column('core_user', 'canLogin', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'Group.deleted'
        db.alter_column('core_group', 'deleted', self.gf('django.db.models.fields.BooleanField')(blank=True))


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
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'verb': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'core.company': {
            'Meta': {'object_name': 'Company'},
            'adminGroup': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'companiesWhereAdmin'", 'null': 'True', 'to': "orm['core.Group']"}),
            'allEmployeesGroup': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'companiesWhereAllEmployeed'", 'null': 'True', 'to': "orm['core.Group']"}),
            'daysIntoNextMonthHourRegistration': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'hoursNeededFor100overtimePay': ('django.db.models.fields.IntegerField', [], {'default': '240'}),
            'hoursNeededFor50overtimePay': ('django.db.models.fields.IntegerField', [], {'default': '160'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'periodeHourRegistrations': ('django.db.models.fields.CharField', [], {'default': "'m'", 'max_length': '1'})
        },
        'core.group': {
            'Meta': {'object_name': 'Group'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'groups'", 'null': 'True', 'to': "orm['core.Company']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'groups'", 'symmetrical': 'False', 'to': "orm['core.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'null': 'True', 'to': "orm['core.Group']"})
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
            'actions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Action']", 'symmetrical': 'False'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'permissions'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'from_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'permissions'", 'null': 'True', 'to': "orm['core.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'negative': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'permissions'", 'null': 'True', 'to': "orm['core.Role']"}),
            'to_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
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
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'hourly_rate': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'percent_cover': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'profileImage': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'validEditHourRegistrationsExpireDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'validEditHourRegistrationsFromDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'validEditHourRegistrationsToDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        }
    }

    complete_apps = ['core']
