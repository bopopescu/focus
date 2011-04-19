# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'HourRegistration'
        db.create_table('hourregistrations_hourregistration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trashed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 4, 19, 3, 2, 37, 782112))),
            ('date_edited', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 4, 19, 3, 2, 37, 782140))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='hourregistration_created', null=True, blank=True, to=orm['user.User'])),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='hourregistration_edited', null=True, blank=True, to=orm['user.User'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='hourregistration_companies', null=True, blank=True, to=orm['company.Company'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['orders.Order'], blank=True)),
            ('time_start', self.gf('django.db.models.fields.CharField')(default='', max_length=5, null=True, blank=True)),
            ('time_end', self.gf('django.db.models.fields.CharField')(default='', max_length=5, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('pause', self.gf('django.db.models.fields.DecimalField')(default='0.5', max_digits=5, decimal_places=3, blank=True)),
            ('hourly_rate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=3, blank=True)),
            ('percent_cover', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=3, blank=True)),
            ('hours_worked', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=3, blank=True)),
            ('savedHours', self.gf('django.db.models.fields.DecimalField')(default='0.0', null=True, max_digits=5, decimal_places=3, blank=True)),
            ('usedOfSavedHours', self.gf('django.db.models.fields.DecimalField')(default='0.0', null=True, max_digits=5, decimal_places=3, blank=True)),
        ))
        db.send_create_signal('hourregistrations', ['HourRegistration'])

        # Adding model 'HourRegisrationImage'
        db.create_table('hourregistrations_hourregisrationimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trashed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 4, 19, 3, 2, 37, 782112))),
            ('date_edited', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 4, 19, 3, 2, 37, 782140))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='hourregisrationimage_created', null=True, blank=True, to=orm['user.User'])),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='hourregisrationimage_edited', null=True, blank=True, to=orm['user.User'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='hourregisrationimage_companies', null=True, blank=True, to=orm['company.Company'])),
        ))
        db.send_create_signal('hourregistrations', ['HourRegisrationImage'])

        # Adding model 'Disbursement'
        db.create_table('hourregistrations_disbursement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trashed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 4, 19, 3, 2, 37, 782112))),
            ('date_edited', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 4, 19, 3, 2, 37, 782140))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='disbursement_created', null=True, blank=True, to=orm['user.User'])),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='disbursement_edited', null=True, blank=True, to=orm['user.User'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='disbursement_companies', null=True, blank=True, to=orm['company.Company'])),
            ('HourRegistration', self.gf('django.db.models.fields.related.ForeignKey')(related_name='disbursements', to=orm['hourregistrations.HourRegistration'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('hourregistrations', ['Disbursement'])

        # Adding model 'DrivingRegistration'
        db.create_table('hourregistrations_drivingregistration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trashed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 4, 19, 3, 2, 37, 782112))),
            ('date_edited', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 4, 19, 3, 2, 37, 782140))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='drivingregistration_created', null=True, blank=True, to=orm['user.User'])),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='drivingregistration_edited', null=True, blank=True, to=orm['user.User'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='drivingregistration_companies', null=True, blank=True, to=orm['company.Company'])),
            ('HourRegistration', self.gf('django.db.models.fields.related.ForeignKey')(related_name='drivingregistration', to=orm['hourregistrations.HourRegistration'])),
            ('time_start', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('time_end', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('kilometres', self.gf('django.db.models.fields.IntegerField')()),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('hourregistrations', ['DrivingRegistration'])


    def backwards(self, orm):
        
        # Deleting model 'HourRegistration'
        db.delete_table('hourregistrations_hourregistration')

        # Deleting model 'HourRegisrationImage'
        db.delete_table('hourregistrations_hourregisrationimage')

        # Deleting model 'Disbursement'
        db.delete_table('hourregistrations_disbursement')

        # Deleting model 'DrivingRegistration'
        db.delete_table('hourregistrations_drivingregistration')


    models = {
        'company.company': {
            'Meta': {'object_name': 'Company'},
            'adminGroup': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'companiesWhereAdmin'", 'null': 'True', 'to': "orm['group.Group']"}),
            'allEmployeesGroup': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'companiesWhereAllEmployeed'", 'null': 'True', 'to': "orm['group.Group']"}),
            'daysIntoNextMonthHourRegistration': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'hoursNeededFor100overtimePay': ('django.db.models.fields.IntegerField', [], {'default': '240'}),
            'hoursNeededFor50overtimePay': ('django.db.models.fields.IntegerField', [], {'default': '160'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'contacts.contact': {
            'Meta': {'object_name': 'Contact'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'contact_companies'", 'null': 'True', 'blank': 'True', 'to': "orm['company.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'contact_created'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 19, 3, 2, 37, 782112)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 19, 3, 2, 37, 782140)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'contact_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '80'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'phone_mobile': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'phone_office': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.comment': {
            'Meta': {'ordering': "['date_created']", 'object_name': 'Comment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'comment_companies'", 'null': 'True', 'blank': 'True', 'to': "orm['company.Company']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'comment_created'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 19, 3, 2, 37, 782112)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 19, 3, 2, 37, 782140)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'comment_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'customers.customer': {
            'Meta': {'object_name': 'Customer'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'cid': ('django.db.models.fields.IntegerField', [], {}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'customer_companies'", 'null': 'True', 'blank': 'True', 'to': "orm['company.Company']"}),
            'contacts': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'customers'", 'blank': 'True', 'to': "orm['contacts.Contact']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'customer_created'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 19, 3, 2, 37, 782112)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 19, 3, 2, 37, 782140)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'customer_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '80'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_address': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'invoice_city': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'invoice_zip': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'})
        },
        'group.group': {
            'Meta': {'object_name': 'Group'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'groups'", 'null': 'True', 'to': "orm['company.Company']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'groups'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['user.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'null': 'True', 'to': "orm['group.Group']"})
        },
        'hourregistrations.disbursement': {
            'HourRegistration': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'disbursements'", 'to': "orm['hourregistrations.HourRegistration']"}),
            'Meta': {'object_name': 'Disbursement'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'disbursement_companies'", 'null': 'True', 'blank': 'True', 'to': "orm['company.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'disbursement_created'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 19, 3, 2, 37, 782112)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 19, 3, 2, 37, 782140)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'disbursement_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'hourregistrations.drivingregistration': {
            'HourRegistration': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'drivingregistration'", 'to': "orm['hourregistrations.HourRegistration']"}),
            'Meta': {'object_name': 'DrivingRegistration'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'drivingregistration_companies'", 'null': 'True', 'blank': 'True', 'to': "orm['company.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'drivingregistration_created'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 19, 3, 2, 37, 782112)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 19, 3, 2, 37, 782140)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'drivingregistration_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kilometres': ('django.db.models.fields.IntegerField', [], {}),
            'time_end': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'time_start': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'hourregistrations.hourregisrationimage': {
            'Meta': {'object_name': 'HourRegisrationImage'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'hourregisrationimage_companies'", 'null': 'True', 'blank': 'True', 'to': "orm['company.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'hourregisrationimage_created'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 19, 3, 2, 37, 782112)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 19, 3, 2, 37, 782140)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'hourregisrationimage_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'hourregistrations.hourregistration': {
            'Meta': {'object_name': 'HourRegistration'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'hourregistration_companies'", 'null': 'True', 'blank': 'True', 'to': "orm['company.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'hourregistration_created'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 19, 3, 2, 37, 782112)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 19, 3, 2, 37, 782140)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'hourregistration_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'hourly_rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '3', 'blank': 'True'}),
            'hours_worked': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '3', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['orders.Order']", 'blank': 'True'}),
            'pause': ('django.db.models.fields.DecimalField', [], {'default': "'0.5'", 'max_digits': '5', 'decimal_places': '3', 'blank': 'True'}),
            'percent_cover': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '3', 'blank': 'True'}),
            'savedHours': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'null': 'True', 'max_digits': '5', 'decimal_places': '3', 'blank': 'True'}),
            'time_end': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'time_start': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'usedOfSavedHours': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'null': 'True', 'max_digits': '5', 'decimal_places': '3', 'blank': 'True'})
        },
        'orders.order': {
            'Meta': {'object_name': 'Order'},
            'POnumber': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'order_companies'", 'null': 'True', 'blank': 'True', 'to': "orm['company.Company']"}),
            'contacts': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'orders'", 'blank': 'True', 'to': "orm['contacts.Contact']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'order_created'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'orders'", 'null': 'True', 'to': "orm['customers.Customer']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 19, 3, 2, 37, 782112)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 19, 3, 2, 37, 782140)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'deliveryAddress': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
            'delivery_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'delivery_date_deadline': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'order_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'oid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'order_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'orders'", 'null': 'True', 'to': "orm['projects.Project']"}),
            'responsible': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ordersWhereResponsible'", 'to': "orm['user.User']"}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'projects.project': {
            'Meta': {'object_name': 'Project'},
            'POnumber': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'project_companies'", 'null': 'True', 'blank': 'True', 'to': "orm['company.Company']"}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects'", 'null': 'True', 'to': "orm['contacts.Contact']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'project_created'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'projects'", 'null': 'True', 'to': "orm['customers.Customer']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 19, 3, 2, 37, 782112)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 19, 3, 2, 37, 782140)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'deliveryAddress': ('django.db.models.fields.TextField', [], {'max_length': '150', 'null': 'True'}),
            'deliveryDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deliveryDateDeadline': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'project_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pid': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'project_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'responsible': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projectsWhereResponsible'", 'null': 'True', 'to': "orm['user.User']"}),
            'trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'user.user': {
            'Meta': {'object_name': 'User'},
            'birthdate': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'canLogin': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_user_users'", 'null': 'True', 'to': "orm['company.Company']"}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'hourly_rate': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'percent_cover': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'profileImage': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'validEditHourRegistrationsFromDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'validEditHourRegistrationsToDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        }
    }

    complete_apps = ['hourregistrations']
