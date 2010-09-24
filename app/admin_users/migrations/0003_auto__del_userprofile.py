# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'UserProfile'
        db.delete_table('admin_users_userprofile')

        # Removing M2M table for field company on 'UserProfile'
        db.delete_table('admin_users_userprofile_company')


    def backwards(self, orm):
        
        # Adding model 'UserProfile'
        db.create_table('admin_users_userprofile', (
            ('home_address', self.gf('django.db.models.fields.TextField')()),
            ('user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('admin_users', ['UserProfile'])

        # Adding M2M table for field company on 'UserProfile'
        db.create_table('admin_users_userprofile_company', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['admin_users.userprofile'], null=False)),
            ('company', models.ForeignKey(orm['companies.company'], null=False))
        ))
        db.create_unique('admin_users_userprofile_company', ['userprofile_id', 'company_id'])


    models = {
        
    }

    complete_apps = ['admin_users']
