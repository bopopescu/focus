# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Valuta'
        db.create_table('stock_valuta', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2010, 10, 29, 2, 43, 45, 132575))),
            ('date_edited', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2010, 10, 29, 2, 43, 45, 132608))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='valuta_created', null=True, blank=True, to=orm['auth.User'])),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='valuta_edited', null=True, blank=True, to=orm['auth.User'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='valuta_edited', null=True, blank=True, to=orm['core.Company'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('currentValue', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal('stock', ['Valuta'])

        # Adding model 'UnitsForSizes'
        db.create_table('stock_unitsforsizes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2010, 10, 29, 2, 43, 45, 132575))),
            ('date_edited', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2010, 10, 29, 2, 43, 45, 132608))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='unitsforsizes_created', null=True, blank=True, to=orm['auth.User'])),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='unitsforsizes_edited', null=True, blank=True, to=orm['auth.User'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='unitsforsizes_edited', null=True, blank=True, to=orm['core.Company'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('stock', ['UnitsForSizes'])

        # Adding model 'ProductGroup'
        db.create_table('stock_productgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2010, 10, 29, 2, 43, 45, 132575))),
            ('date_edited', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2010, 10, 29, 2, 43, 45, 132608))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='productgroup_created', null=True, blank=True, to=orm['auth.User'])),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='productgroup_edited', null=True, blank=True, to=orm['auth.User'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='productgroup_edited', null=True, blank=True, to=orm['core.Company'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('stock', ['ProductGroup'])

        # Adding model 'Product'
        db.create_table('stock_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2010, 10, 29, 2, 43, 45, 132575))),
            ('date_edited', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2010, 10, 29, 2, 43, 45, 132608))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='product_created', null=True, blank=True, to=orm['auth.User'])),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='product_edited', null=True, blank=True, to=orm['auth.User'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='product_edited', null=True, blank=True, to=orm['core.Company'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('countOfAvailableInStock', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='products', to=orm['stock.ProductGroup'])),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('unitForSize', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stock.UnitsForSizes'])),
            ('price', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('priceVal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='products', to=orm['stock.Valuta'])),
        ))
        db.send_create_signal('stock', ['Product'])


    def backwards(self, orm):
        
        # Deleting model 'Valuta'
        db.delete_table('stock_valuta')

        # Deleting model 'UnitsForSizes'
        db.delete_table('stock_unitsforsizes')

        # Deleting model 'ProductGroup'
        db.delete_table('stock_productgroup')

        # Deleting model 'Product'
        db.delete_table('stock_product')


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
        'stock.product': {
            'Meta': {'object_name': 'Product'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'product_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'countOfAvailableInStock': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'product_created'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 10, 29, 2, 43, 45, 132575)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 10, 29, 2, 43, 45, 132608)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'product_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products'", 'to': "orm['stock.ProductGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'priceVal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products'", 'to': "orm['stock.Valuta']"}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'unitForSize': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stock.UnitsForSizes']"})
        },
        'stock.productgroup': {
            'Meta': {'object_name': 'ProductGroup'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'productgroup_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'productgroup_created'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 10, 29, 2, 43, 45, 132575)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 10, 29, 2, 43, 45, 132608)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'productgroup_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'stock.unitsforsizes': {
            'Meta': {'object_name': 'UnitsForSizes'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'unitsforsizes_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'unitsforsizes_created'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 10, 29, 2, 43, 45, 132575)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 10, 29, 2, 43, 45, 132608)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'unitsforsizes_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'stock.valuta': {
            'Meta': {'object_name': 'Valuta'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'valuta_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'valuta_created'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'currentValue': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 10, 29, 2, 43, 45, 132575)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 10, 29, 2, 43, 45, 132608)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'valuta_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['stock']
