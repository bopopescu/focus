# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'RepeatOption'
        db.create_table('calendar_repeatoption', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trashed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 11, 1, 0, 48, 11, 718285))),
            ('date_edited', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 11, 1, 0, 48, 11, 718316))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='repeatoption_created', null=True, blank=True, to=orm['user.User'])),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='repeatoption_edited', null=True, blank=True, to=orm['user.User'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='repeatoption_companies', null=True, blank=True, to=orm['company.Company'])),
            ('available_option', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('times', self.gf('django.db.models.fields.IntegerField')()),
            ('repeat_until', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal('calendar', ['RepeatOption'])

        # Adding model 'Event'
        db.create_table('calendar_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trashed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 11, 1, 0, 48, 11, 718285))),
            ('date_edited', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 11, 1, 0, 48, 11, 718316))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='event_created', null=True, blank=True, to=orm['user.User'])),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='event_edited', null=True, blank=True, to=orm['user.User'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='event_companies', null=True, blank=True, to=orm['company.Company'])),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('repeat', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['calendar.RepeatOption'])),
        ))
        db.send_create_signal('calendar', ['Event'])

        # Adding M2M table for field users on 'Event'
        db.create_table('calendar_event_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['calendar.event'], null=False)),
            ('user', models.ForeignKey(orm['user.user'], null=False))
        ))
        db.create_unique('calendar_event_users', ['event_id', 'user_id'])

        # Adding M2M table for field special_cases on 'Event'
        db.create_table('calendar_event_special_cases', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_event', models.ForeignKey(orm['calendar.event'], null=False)),
            ('to_event', models.ForeignKey(orm['calendar.event'], null=False))
        ))
        db.create_unique('calendar_event_special_cases', ['from_event_id', 'to_event_id'])


    def backwards(self, orm):
        
        # Deleting model 'RepeatOption'
        db.delete_table('calendar_repeatoption')

        # Deleting model 'Event'
        db.delete_table('calendar_event')

        # Removing M2M table for field users on 'Event'
        db.delete_table('calendar_event_users')

        # Removing M2M table for field special_cases on 'Event'
        db.delete_table('calendar_event_special_cases')


    models = {
        'calendar.event': {
            'Meta': {'object_name': 'Event'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'event_companies'", 'null': 'True', 'blank': 'True', 'to': "orm['company.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'event_created'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 11, 1, 0, 48, 11, 718285)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 11, 1, 0, 48, 11, 718316)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'event_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'repeat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['calendar.RepeatOption']"}),
            'special_cases': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'parent_event'", 'symmetrical': 'False', 'to': "orm['calendar.Event']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'events'", 'symmetrical': 'False', 'to': "orm['user.User']"})
        },
        'calendar.repeatoption': {
            'Meta': {'object_name': 'RepeatOption'},
            'available_option': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'repeatoption_companies'", 'null': 'True', 'blank': 'True', 'to': "orm['company.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'repeatoption_created'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 11, 1, 0, 48, 11, 718285)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 11, 1, 0, 48, 11, 718316)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'repeatoption_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'repeat_until': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'times': ('django.db.models.fields.IntegerField', [], {}),
            'trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'company.company': {
            'Meta': {'object_name': 'Company'},
            'admin_group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'companiesWhereAdmin'", 'null': 'True', 'to': "orm['group.Group']"}),
            'all_employees_group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'companiesWhereAllEmployeed'", 'null': 'True', 'to': "orm['group.Group']"}),
            'days_into_next_month_hourregistration': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'email_address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'email_host': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'email_password': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'email_username': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'hours_needed_for_100_overtime_pay': ('django.db.models.fields.IntegerField', [], {'default': '240'}),
            'hours_needed_for_50_overtime_pay': ('django.db.models.fields.IntegerField', [], {'default': '160'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
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
            'language': ('django.db.models.fields.CharField', [], {'default': "'nb'", 'max_length': '30'}),
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

    complete_apps = ['calendar']
