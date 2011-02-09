# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TicketStatus'
        db.create_table('tickets_ticketstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trashed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 2, 9, 16, 52, 36, 191880))),
            ('date_edited', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 2, 9, 16, 52, 36, 191916))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='ticketstatus_created', null=True, blank=True, to=orm['core.User'])),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='ticketstatus_edited', null=True, blank=True, to=orm['core.User'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='ticketstatus_edited', null=True, blank=True, to=orm['core.Company'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('order_priority', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('tickets', ['TicketStatus'])

        # Adding model 'TicketPriority'
        db.create_table('tickets_ticketpriority', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trashed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 2, 9, 16, 52, 36, 191880))),
            ('date_edited', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 2, 9, 16, 52, 36, 191916))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='ticketpriority_created', null=True, blank=True, to=orm['core.User'])),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='ticketpriority_edited', null=True, blank=True, to=orm['core.User'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='ticketpriority_edited', null=True, blank=True, to=orm['core.Company'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('tickets', ['TicketPriority'])

        # Adding model 'TicketType'
        db.create_table('tickets_tickettype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trashed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 2, 9, 16, 52, 36, 191880))),
            ('date_edited', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 2, 9, 16, 52, 36, 191916))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='tickettype_created', null=True, blank=True, to=orm['core.User'])),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='tickettype_edited', null=True, blank=True, to=orm['core.User'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='tickettype_edited', null=True, blank=True, to=orm['core.Company'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('tickets', ['TicketType'])

        # Adding model 'Ticket'
        db.create_table('tickets_ticket', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trashed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 2, 9, 16, 52, 36, 191880))),
            ('date_edited', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 2, 9, 16, 52, 36, 191916))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='ticket_created', null=True, blank=True, to=orm['core.User'])),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='ticket_edited', null=True, blank=True, to=orm['core.User'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='ticket_edited', null=True, blank=True, to=orm['core.Company'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tickets.TicketStatus'])),
            ('priority', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tickets.TicketPriority'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tickets.TicketType'])),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['customers.Customer'])),
            ('assigned_to', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.User'], null=True, blank=True)),
        ))
        db.send_create_signal('tickets', ['Ticket'])

        # Adding model 'Comment'
        db.create_table('tickets_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trashed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 2, 9, 16, 52, 36, 191880))),
            ('date_edited', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 2, 9, 16, 52, 36, 191916))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='comment_created', null=True, blank=True, to=orm['core.User'])),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='comment_edited', null=True, blank=True, to=orm['core.User'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='comment_edited', null=True, blank=True, to=orm['core.Company'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('Ticket', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comments', to=orm['tickets.Ticket'])),
        ))
        db.send_create_signal('tickets', ['Comment'])


    def backwards(self, orm):
        
        # Deleting model 'TicketStatus'
        db.delete_table('tickets_ticketstatus')

        # Deleting model 'TicketPriority'
        db.delete_table('tickets_ticketpriority')

        # Deleting model 'TicketType'
        db.delete_table('tickets_tickettype')

        # Deleting model 'Ticket'
        db.delete_table('tickets_ticket')

        # Deleting model 'Comment'
        db.delete_table('tickets_comment')


    models = {
        'contacts.contact': {
            'Meta': {'object_name': 'Contact'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'contact_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'contact_created'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 2, 9, 16, 52, 36, 191880)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 2, 9, 16, 52, 36, 191916)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'contact_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '80'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
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
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'groups'", 'symmetrical': 'False', 'to': "orm['core.User']"}),
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
            'profileImage': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
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
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 2, 9, 16, 52, 36, 191880)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 2, 9, 16, 52, 36, 191916)'}),
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
        'tickets.comment': {
            'Meta': {'ordering': "['date_created']", 'object_name': 'Comment'},
            'Ticket': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': "orm['tickets.Ticket']"}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'comment_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'comment_created'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 2, 9, 16, 52, 36, 191880)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 2, 9, 16, 52, 36, 191916)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'comment_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'tickets.ticket': {
            'Meta': {'ordering': "['status', 'date_created']", 'object_name': 'Ticket'},
            'assigned_to': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.User']", 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'ticket_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'ticket_created'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['customers.Customer']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 2, 9, 16, 52, 36, 191880)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 2, 9, 16, 52, 36, 191916)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'ticket_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'priority': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tickets.TicketPriority']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tickets.TicketStatus']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tickets.TicketType']"})
        },
        'tickets.ticketpriority': {
            'Meta': {'object_name': 'TicketPriority'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'ticketpriority_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'ticketpriority_created'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 2, 9, 16, 52, 36, 191880)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 2, 9, 16, 52, 36, 191916)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'ticketpriority_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'tickets.ticketstatus': {
            'Meta': {'ordering': "['order_priority']", 'object_name': 'TicketStatus'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'ticketstatus_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'ticketstatus_created'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 2, 9, 16, 52, 36, 191880)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 2, 9, 16, 52, 36, 191916)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'ticketstatus_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'order_priority': ('django.db.models.fields.IntegerField', [], {}),
            'trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'tickets.tickettype': {
            'Meta': {'object_name': 'TicketType'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'tickettype_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'tickettype_created'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 2, 9, 16, 52, 36, 191880)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 2, 9, 16, 52, 36, 191916)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'tickettype_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['tickets']
