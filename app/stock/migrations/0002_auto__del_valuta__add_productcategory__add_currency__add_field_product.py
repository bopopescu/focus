# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Valuta'
        db.delete_table('stock_valuta')

        # Adding model 'ProductCategory'
        db.create_table('stock_productcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2010, 10, 30, 3, 49, 29, 657144))),
            ('date_edited', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2010, 10, 30, 3, 49, 29, 657181))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='productcategory_created', null=True, blank=True, to=orm['auth.User'])),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='productcategory_edited', null=True, blank=True, to=orm['auth.User'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='productcategory_edited', null=True, blank=True, to=orm['core.Company'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('stock', ['ProductCategory'])

        # Adding model 'Currency'
        db.create_table('stock_currency', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2010, 10, 30, 3, 49, 29, 657144))),
            ('date_edited', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2010, 10, 30, 3, 49, 29, 657181))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='currency_created', null=True, blank=True, to=orm['auth.User'])),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='currency_edited', null=True, blank=True, to=orm['auth.User'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='currency_edited', null=True, blank=True, to=orm['core.Company'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('sign', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('stock', ['Currency'])

        # Adding field 'ProductGroup.category'
        db.add_column('stock_productgroup', 'category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='productgroups', null=True, to=orm['stock.ProductCategory']), keep_default=False)

        # Adding field 'Product.pid'
        db.add_column('stock_product', 'pid', self.gf('django.db.models.fields.IntegerField')(null=True), keep_default=False)

        # Adding field 'Product.description'
        db.add_column('stock_product', 'description', self.gf('django.db.models.fields.TextField')(null=True), keep_default=False)

        # Adding field 'Product.price_out'
        db.add_column('stock_product', 'price_out', self.gf('django.db.models.fields.CharField')(max_length=100, null=True), keep_default=False)

        # Adding field 'Product.max_discount'
        db.add_column('stock_product', 'max_discount', self.gf('django.db.models.fields.CharField')(max_length=5, null=True), keep_default=False)

        # Adding field 'Product.supplier'
        db.add_column('stock_product', 'supplier', self.gf('django.db.models.fields.related.ForeignKey')(related_name='products', null=True, to=orm['suppliers.Supplier']), keep_default=False)

        # Changing field 'Product.priceVal'
        db.alter_column('stock_product', 'priceVal_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stock.Currency']))

        # Changing field 'Product.price'
        db.alter_column('stock_product', 'price', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))


    def backwards(self, orm):
        
        # Adding model 'Valuta'
        db.create_table('stock_valuta', (
            ('currentValue', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='valuta_edited', null=True, to=orm['auth.User'], blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='valuta_created', null=True, to=orm['auth.User'], blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2010, 10, 29, 2, 43, 45, 132575))),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='valuta_edited', null=True, to=orm['core.Company'], blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_edited', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2010, 10, 29, 2, 43, 45, 132608))),
        ))
        db.send_create_signal('stock', ['Valuta'])

        # Deleting model 'ProductCategory'
        db.delete_table('stock_productcategory')

        # Deleting model 'Currency'
        db.delete_table('stock_currency')

        # Deleting field 'ProductGroup.category'
        db.delete_column('stock_productgroup', 'category_id')

        # Deleting field 'Product.pid'
        db.delete_column('stock_product', 'pid')

        # Deleting field 'Product.description'
        db.delete_column('stock_product', 'description')

        # Deleting field 'Product.price_out'
        db.delete_column('stock_product', 'price_out')

        # Deleting field 'Product.max_discount'
        db.delete_column('stock_product', 'max_discount')

        # Deleting field 'Product.supplier'
        db.delete_column('stock_product', 'supplier_id')

        # Changing field 'Product.priceVal'
        db.alter_column('stock_product', 'priceVal_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stock.Valuta']))

        # Changing field 'Product.price'
        db.alter_column('stock_product', 'price', self.gf('django.db.models.fields.CharField')(max_length=100))


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
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 10, 30, 3, 49, 29, 657144)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 10, 30, 3, 49, 29, 657181)'}),
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
        'stock.currency': {
            'Meta': {'object_name': 'Currency'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'currency_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'currency_created'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 10, 30, 3, 49, 29, 657144)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 10, 30, 3, 49, 29, 657181)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'currency_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sign': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'stock.product': {
            'Meta': {'object_name': 'Product'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'product_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'countOfAvailableInStock': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'product_created'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 10, 30, 3, 49, 29, 657144)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 10, 30, 3, 49, 29, 657181)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'product_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products'", 'to': "orm['stock.ProductGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_discount': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pid': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'price': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'priceVal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products'", 'to': "orm['stock.Currency']"}),
            'price_out': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products'", 'null': 'True', 'to': "orm['suppliers.Supplier']"}),
            'unitForSize': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stock.UnitsForSizes']"})
        },
        'stock.productcategory': {
            'Meta': {'object_name': 'ProductCategory'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'productcategory_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'productcategory_created'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 10, 30, 3, 49, 29, 657144)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 10, 30, 3, 49, 29, 657181)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'productcategory_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'stock.productgroup': {
            'Meta': {'object_name': 'ProductGroup'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'productgroups'", 'null': 'True', 'to': "orm['stock.ProductCategory']"}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'productgroup_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'productgroup_created'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 10, 30, 3, 49, 29, 657144)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 10, 30, 3, 49, 29, 657181)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'productgroup_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'stock.unitsforsizes': {
            'Meta': {'object_name': 'UnitsForSizes'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'unitsforsizes_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'unitsforsizes_created'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 10, 30, 3, 49, 29, 657144)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 10, 30, 3, 49, 29, 657181)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'unitsforsizes_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'suppliers.supplier': {
            'Meta': {'object_name': 'Supplier'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'supplier_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'contacts': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'suppliers'", 'symmetrical': 'False', 'to': "orm['contacts.Contact']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'supplier_created'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 10, 30, 3, 49, 29, 657144)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 10, 30, 3, 49, 29, 657181)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'supplier_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['stock']
