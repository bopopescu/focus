# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Project.deliveryAddress'
        db.alter_column('projects_project', 'deliveryAddress', self.gf('django.db.models.fields.TextField')(max_length=150, null=True))


    def backwards(self, orm):
        
        # Changing field 'Project.deliveryAddress'
        db.alter_column('projects_project', 'deliveryAddress', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))


    models = {
        'contacts.contact': {
            'Meta': {'object_name': 'Contact'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'contact_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'contact_created'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 4, 20, 57, 24, 572712)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 4, 20, 57, 24, 572752)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'contact_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '80'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
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
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'comment_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'comment_created'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 4, 20, 57, 24, 572712)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 4, 20, 57, 24, 572752)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'comment_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'core.company': {
            'Meta': {'object_name': 'Company'},
            'adminGroup': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'companiesWhereAdmin'", 'null': 'True', 'to': "orm['core.Group']"}),
            'allEmployeesGroup': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'companiesWhereAllEmployeed'", 'null': 'True', 'to': "orm['core.Group']"}),
            'daysIntoNextMonthHourRegistration': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'hoursNeededFor100overtimePay': ('django.db.models.fields.IntegerField', [], {'default': '240'}),
            'hoursNeededFor50overtimePay': ('django.db.models.fields.IntegerField', [], {'default': '160'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'core.group': {
            'Meta': {'object_name': 'Group'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'groups'", 'null': 'True', 'to': "orm['core.Company']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'groups'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['core.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'null': 'True', 'to': "orm['core.Group']"})
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
            'profileImage': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'validEditHourRegistrationsFromDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'validEditHourRegistrationsToDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        'customers.customer': {
            'Meta': {'object_name': 'Customer'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'alternative_address': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'cid': ('django.db.models.fields.IntegerField', [], {}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'customer_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'contacts': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'customers'", 'blank': 'True', 'to': "orm['contacts.Contact']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'customer_created'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 4, 20, 57, 24, 572712)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 4, 20, 57, 24, 572752)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'customer_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '80'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'})
        },
        'projects.milestone': {
            'Meta': {'object_name': 'Milestone'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'milestone_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'milestone_created'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 4, 20, 57, 24, 572712)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 4, 20, 57, 24, 572752)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'milestone_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'milestones'", 'to': "orm['projects.Project']"}),
            'trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'projects.project': {
            'Meta': {'object_name': 'Project'},
            'POnumber': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'project_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'project_created'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'projects'", 'null': 'True', 'to': "orm['customers.Customer']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 4, 20, 57, 24, 572712)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 4, 20, 57, 24, 572752)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'deliveryAddress': ('django.db.models.fields.TextField', [], {'max_length': '150', 'null': 'True'}),
            'deliveryDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deliveryDateDeadline': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'project_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pid': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'project_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'responsible': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projectsWhereResponsible'", 'null': 'True', 'to': "orm['core.User']"}),
            'trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'projects.projectfile': {
            'Meta': {'object_name': 'ProjectFile'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'projectfile_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'projectfile_created'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 4, 20, 57, 24, 572712)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 4, 20, 57, 24, 572752)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'projectfile_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'folder': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'files'", 'to': "orm['projects.ProjectFolder']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'project_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'files'", 'to': "orm['projects.Project']"}),
            'trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'projects.projectfolder': {
            'Meta': {'object_name': 'ProjectFolder'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'projectfolder_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'projectfolder_created'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 4, 20, 57, 24, 572712)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 4, 20, 57, 24, 572752)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'projectfolder_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'project_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'folders'", 'to': "orm['projects.Project']"}),
            'trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['projects']