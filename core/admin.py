from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin as FPAdmin

from core.models import ObjectPermission

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

class FlatPageAdmin(ObjectPermissionMixin, FPAdmin):
    inlines = FPAdmin.inlines + [ObjectPermissionInline]

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)