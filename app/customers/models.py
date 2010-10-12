from django.db import models
from django.contrib import admin
from app.contacts.models import Contact
from core.admin import *
from django.contrib.auth.models import User
from django.contrib.contenttypes.generic import GenericTabularInline
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin as FPAdmin
from core.models import ObjectPermission, PersistentModel
from django.core import urlresolvers

class Customer(PersistentModel):
    full_name = models.CharField("Fullt navn", max_length=80)
    email = models.EmailField("Epostadresse", max_length=80)
    address = models.CharField("Adresse", max_length=80, blank=True)
    phone = models.CharField("Telefon", max_length=20, blank=True)
    zip = models.CharField("Postnr", max_length=4, blank=True)
    city = models.CharField("By", max_length=20, blank=True)

    alternative_address = models.CharField("Alternativ adresse", max_length=20, blank=True)
    owner = models.ForeignKey(User, blank=True, related_name="UsersContacts");
    contacts = models.ManyToManyField(Contact, blank=True, related_name="customers", verbose_name="Kontakter")

    def __unicode__(self):
        return self.full_name

    def get_url(self):
        return urlresolvers.reverse('app.customers.views.view', args=("%s" % self.id,))

class ObjectPermissionInline(GenericTabularInline):
    model = ObjectPermission
    raw_id_fields = ['user']

class ObjectPermissionMixin(object):
    def has_change_permission(self, request, obj=None):
        opts = self.opts
        return request.user.has_perm(opts.app_label + '.' + opts.get_change_permission(), obj)

    def has_delete_permission(self, request, obj=None):
        opts = self.opts
        return request.user.has_perm(opts.app_label + '.' + opts.get_delete_permission(), obj)

from reversion.admin import VersionAdmin

class CustomerAdmin(VersionAdmin, admin.ModelAdmin, ObjectPermissionMixin):
    inlines = [ObjectPermissionInline]

admin.site.register(Customer, CustomerAdmin)

