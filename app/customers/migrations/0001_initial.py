# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Customer'
        db.create_table('customers_customer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2010, 9, 12, 16, 53, 51, 593206))),
            ('date_edited', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2010, 9, 12, 16, 53, 51, 593243))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='customer_created', null=True, blank=True, to=orm['auth.User'])),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='customer_edited', null=True, blank=True, to=orm['auth.User'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='customer_edited', null=True, blank=True, to=orm['core.Company'])),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=80)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('zip', self.gf('django.db.models.fields.IntegerField')(max_length=4, blank=True)),
            ('birth_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('alternative_address', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='UsersContacts', blank=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('customers', ['Customer'])

        # Adding M2M table for field projects on 'Customer'
        db.create_table('customers_customer_projects', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('customer', models.ForeignKey(orm['customers.customer'], null=False)),
            ('project', models.ForeignKey(orm['projects.project'], null=False))
        ))
        db.create_unique('customers_customer_projects', ['customer_id', 'project_id'])

        # Adding M2M table for field contacts on 'Customer'
        db.create_table('customers_customer_contacts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('customer', models.ForeignKey(orm['customers.customer'], null=False)),
            ('contact', models.ForeignKey(orm['contacts.contact'], null=False))
        ))
        db.create_unique('customers_customer_contacts', ['customer_id', 'contact_id'])


    def backwards(self, orm):
        
        # Deleting model 'Customer'
        db.delete_table('customers_customer')

        # Removing M2M table for field projects on 'Customer'
        db.delete_table('customers_customer_projects')

        # Removing M2M table for field contacts on 'Customer'
        db.delete_table('customers_customer_contacts')


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
        'contacts.contact': {
            'Meta': {'object_name': 'Contact'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'contact_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'contact_created'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 9, 12, 16, 53, 51, 593206)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 9, 12, 16, 53, 51, 593243)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'contact_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '80'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'})
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
        'customers.customer': {
            'Meta': {'object_name': 'Customer'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'alternative_address': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'customer_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'contacts': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'customers'", 'blank': 'True', 'to': "orm['contacts.Contact']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'customer_created'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 9, 12, 16, 53, 51, 593206)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 9, 12, 16, 53, 51, 593243)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'customer_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '80'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'UsersContacts'", 'blank': 'True', 'to': "orm['auth.User']"}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'projects': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'customers'", 'blank': 'True', 'to': "orm['projects.Project']"}),
            'zip': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'blank': 'True'})
        },
        'projects.project': {
            'Meta': {'object_name': 'Project'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'project_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'project_created'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 9, 12, 16, 53, 51, 593206)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 9, 12, 16, 53, 51, 593243)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'project_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project_name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        }
    }

    complete_apps = ['customers']
