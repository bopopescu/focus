# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Milestone'
        db.create_table('projects_milestone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 1, 7, 18, 57, 36, 274238))),
            ('date_edited', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 1, 7, 18, 57, 36, 274285))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='milestone_created', null=True, blank=True, to=orm['core.User'])),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='milestone_edited', null=True, blank=True, to=orm['core.User'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='milestone_edited', null=True, blank=True, to=orm['core.Company'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='milestones', to=orm['projects.Project'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('projects', ['Milestone'])

        # Changing field 'ProjectFile.creator'
        db.alter_column('projects_projectfile', 'creator_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, blank=True, to=orm['core.User']))

        # Changing field 'ProjectFile.editor'
        db.alter_column('projects_projectfile', 'editor_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, blank=True, to=orm['core.User']))

        # Adding field 'Project.POnumber'
        db.add_column('projects_project', 'POnumber', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True), keep_default=False)

        # Changing field 'Project.creator'
        db.alter_column('projects_project', 'creator_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, blank=True, to=orm['core.User']))

        # Changing field 'Project.responsible'
        db.alter_column('projects_project', 'responsible_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['core.User']))

        # Changing field 'Project.editor'
        db.alter_column('projects_project', 'editor_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, blank=True, to=orm['core.User']))

        # Changing field 'ProjectFolder.creator'
        db.alter_column('projects_projectfolder', 'creator_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, blank=True, to=orm['core.User']))

        # Changing field 'ProjectFolder.editor'
        db.alter_column('projects_projectfolder', 'editor_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, blank=True, to=orm['core.User']))


    def backwards(self, orm):
        
        # Deleting model 'Milestone'
        db.delete_table('projects_milestone')

        # Changing field 'ProjectFile.creator'
        db.alter_column('projects_projectfile', 'creator_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User'], blank=True))

        # Changing field 'ProjectFile.editor'
        db.alter_column('projects_projectfile', 'editor_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User'], blank=True))

        # Deleting field 'Project.POnumber'
        db.delete_column('projects_project', 'POnumber')

        # Changing field 'Project.creator'
        db.alter_column('projects_project', 'creator_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User'], blank=True))

        # Changing field 'Project.responsible'
        db.alter_column('projects_project', 'responsible_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'Project.editor'
        db.alter_column('projects_project', 'editor_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User'], blank=True))

        # Changing field 'ProjectFolder.creator'
        db.alter_column('projects_projectfolder', 'creator_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User'], blank=True))

        # Changing field 'ProjectFolder.editor'
        db.alter_column('projects_projectfolder', 'editor_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User'], blank=True))


    models = {
        'contacts.contact': {
            'Meta': {'object_name': 'Contact'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'contact_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'contact_created'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 1, 7, 18, 57, 36, 274238)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 1, 7, 18, 57, 36, 274285)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'contact_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '80'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'core.company': {
            'Meta': {'object_name': 'Company'},
            'adminGroup': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'companiesWhereAdmin'", 'null': 'True', 'to': "orm['core.Group']"}),
            'allEmployeesGroup': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'companiesWhereAllEmployeed'", 'null': 'True', 'to': "orm['core.Group']"}),
            'daysIntoNextMonthTypeOfHourRegistration': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'core.group': {
            'Meta': {'object_name': 'Group'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'groups'", 'null': 'True', 'to': "orm['core.Company']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'groups'", 'symmetrical': 'False', 'to': "orm['core.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'null': 'True', 'to': "orm['core.Group']"})
        },
        'core.user': {
            'Meta': {'object_name': 'User'},
            'canLogin': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'core_user_users'", 'null': 'True', 'to': "orm['core.Company']"}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'daysIntoNextMonthTypeOfHourRegistration': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'daysIntoNextMonthTypeOfHourRegistrationExpire': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'hourly_rate': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'percent_cover': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'profileImage': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
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
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 1, 7, 18, 57, 36, 274238)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 1, 7, 18, 57, 36, 274285)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'customer_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '80'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'})
        },
        'projects.milestone': {
            'Meta': {'object_name': 'Milestone'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'milestone_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'milestone_created'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 1, 7, 18, 57, 36, 274238)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 1, 7, 18, 57, 36, 274285)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'milestone_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'milestones'", 'to': "orm['projects.Project']"})
        },
        'projects.project': {
            'Meta': {'object_name': 'Project'},
            'POnumber': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'project_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'project_created'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'projects'", 'null': 'True', 'to': "orm['customers.Customer']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 1, 7, 18, 57, 36, 274238)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 1, 7, 18, 57, 36, 274285)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'deliveryAddress': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
            'deliveryDate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'deliveryDateDeadline': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'project_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pid': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'project_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'responsible': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projectsWhereResponsible'", 'null': 'True', 'to': "orm['core.User']"})
        },
        'projects.projectfile': {
            'Meta': {'object_name': 'ProjectFile'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'projectfile_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'projectfile_created'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 1, 7, 18, 57, 36, 274238)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 1, 7, 18, 57, 36, 274285)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'projectfile_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'folder': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'files'", 'to': "orm['projects.ProjectFolder']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'project_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'files'", 'to': "orm['projects.Project']"})
        },
        'projects.projectfolder': {
            'Meta': {'object_name': 'ProjectFolder'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'projectfolder_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'projectfolder_created'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 1, 7, 18, 57, 36, 274238)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 1, 7, 18, 57, 36, 274285)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'projectfolder_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'project_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'folders'", 'to': "orm['projects.Project']"})
        }
    }

    complete_apps = ['projects']
