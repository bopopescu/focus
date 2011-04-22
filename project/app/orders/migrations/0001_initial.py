# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Order'
        db.create_table('orders_order', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trashed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 4, 22, 16, 58, 41, 408885))),
            ('date_edited', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 4, 22, 16, 58, 41, 408912))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='order_created', null=True, blank=True, to=orm['user.User'])),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='order_edited', null=True, blank=True, to=orm['user.User'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='order_companies', null=True, blank=True, to=orm['company.Company'])),
            ('oid', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('POnumber', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('order_name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='orders', null=True, to=orm['customers.Customer'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='orders', null=True, to=orm['projects.Project'])),
            ('deliveryAddress', self.gf('django.db.models.fields.CharField')(max_length=150, null=True)),
            ('responsible', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='ordersWhereResponsible', null=True, to=orm['user.User'])),
            ('delivery_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('delivery_date_deadline', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('orders', ['Order'])

        # Adding M2M table for field contacts on 'Order'
        db.create_table('orders_order_contacts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('order', models.ForeignKey(orm['orders.order'], null=False)),
            ('contact', models.ForeignKey(orm['contacts.contact'], null=False))
        ))
        db.create_unique('orders_order_contacts', ['order_id', 'contact_id'])

        # Adding model 'OrderLine'
        db.create_table('orders_orderline', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trashed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 4, 22, 16, 58, 41, 408885))),
            ('date_edited', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 4, 22, 16, 58, 41, 408912))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='orderline_created', null=True, blank=True, to=orm['user.User'])),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='orderline_edited', null=True, blank=True, to=orm['user.User'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='orderline_companies', null=True, blank=True, to=orm['company.Company'])),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(related_name='orderlines', to=orm['orders.Order'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='orderlines', to=orm['stock.Product'])),
            ('count', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('orders', ['OrderLine'])


    def backwards(self, orm):
        
        # Deleting model 'Order'
        db.delete_table('orders_order')

        # Removing M2M table for field contacts on 'Order'
        db.delete_table('orders_order_contacts')

        # Deleting model 'OrderLine'
        db.delete_table('orders_orderline')


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
            'address': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'contact_companies'", 'null': 'True', 'blank': 'True', 'to': "orm['company.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'contact_created'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 22, 16, 58, 41, 408885)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 22, 16, 58, 41, 408912)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'contact_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '80'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            'phone_mobile': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            'phone_office': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
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
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 22, 16, 58, 41, 408885)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 22, 16, 58, 41, 408912)'}),
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
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 22, 16, 58, 41, 408885)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 22, 16, 58, 41, 408912)'}),
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
        'orders.order': {
            'Meta': {'object_name': 'Order'},
            'POnumber': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'order_companies'", 'null': 'True', 'blank': 'True', 'to': "orm['company.Company']"}),
            'contacts': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'orders'", 'blank': 'True', 'to': "orm['contacts.Contact']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'order_created'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'orders'", 'null': 'True', 'to': "orm['customers.Customer']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 22, 16, 58, 41, 408885)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 22, 16, 58, 41, 408912)'}),
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
            'responsible': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ordersWhereResponsible'", 'null': 'True', 'to': "orm['user.User']"}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'orders.orderline': {
            'Meta': {'object_name': 'OrderLine'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'orderline_companies'", 'null': 'True', 'blank': 'True', 'to': "orm['company.Company']"}),
            'count': ('django.db.models.fields.IntegerField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'orderline_created'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 22, 16, 58, 41, 408885)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 22, 16, 58, 41, 408912)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'orderline_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orderlines'", 'to': "orm['orders.Order']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orderlines'", 'to': "orm['stock.Product']"}),
            'trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'projects.project': {
            'Meta': {'object_name': 'Project'},
            'POnumber': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'project_companies'", 'null': 'True', 'blank': 'True', 'to': "orm['company.Company']"}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects'", 'null': 'True', 'to': "orm['contacts.Contact']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'project_created'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'projects'", 'null': 'True', 'to': "orm['customers.Customer']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 22, 16, 58, 41, 408885)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 22, 16, 58, 41, 408912)'}),
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
        'stock.currency': {
            'Meta': {'object_name': 'Currency'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'currency_companies'", 'null': 'True', 'blank': 'True', 'to': "orm['company.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'currency_created'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 22, 16, 58, 41, 408885)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 22, 16, 58, 41, 408912)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'currency_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'value': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2'})
        },
        'stock.product': {
            'Meta': {'object_name': 'Product'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'product_companies'", 'null': 'True', 'blank': 'True', 'to': "orm['company.Company']"}),
            'countOfAvailableInStock': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'product_created'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 22, 16, 58, 41, 408885)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 22, 16, 58, 41, 408912)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'product_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_discount': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'normalDeliveryTime': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'pid': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'price': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'priceVal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products'", 'to': "orm['stock.Currency']"}),
            'price_out': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'productGroup': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products'", 'null': 'True', 'to': "orm['stock.ProductGroup']"}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products'", 'null': 'True', 'to': "orm['suppliers.Supplier']"}),
            'trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'unitForSize': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stock.UnitsForSizes']", 'null': 'True'})
        },
        'stock.productcategory': {
            'Meta': {'object_name': 'ProductCategory'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'productcategory_companies'", 'null': 'True', 'blank': 'True', 'to': "orm['company.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'productcategory_created'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 22, 16, 58, 41, 408885)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 22, 16, 58, 41, 408912)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'productcategory_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'stock.productgroup': {
            'Meta': {'object_name': 'ProductGroup'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'productgroups'", 'null': 'True', 'to': "orm['stock.ProductCategory']"}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'productgroup_companies'", 'null': 'True', 'blank': 'True', 'to': "orm['company.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'productgroup_created'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 22, 16, 58, 41, 408885)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 22, 16, 58, 41, 408912)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'productgroup_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'stock.unitsforsizes': {
            'Meta': {'object_name': 'UnitsForSizes'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'unitsforsizes_companies'", 'null': 'True', 'blank': 'True', 'to': "orm['company.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'unitsforsizes_created'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 22, 16, 58, 41, 408885)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 22, 16, 58, 41, 408912)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'unitsforsizes_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'suppliers.supplier': {
            'Meta': {'object_name': 'Supplier'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'supplier_companies'", 'null': 'True', 'blank': 'True', 'to': "orm['company.Company']"}),
            'contacts': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'suppliers'", 'symmetrical': 'False', 'to': "orm['contacts.Contact']"}),
            'country': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'supplier_created'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 22, 16, 58, 41, 408885)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 22, 16, 58, 41, 408912)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'supplier_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['user.User']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'email_contact': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '75'}),
            'email_order': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'}),
            'trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'zip': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'})
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

    complete_apps = ['orders']
