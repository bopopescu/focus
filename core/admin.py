from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin as FPAdmin
from core.models import *

"""
For auto-version of objects
"""
from reversion.admin import VersionAdmin
class ModelAdmin(VersionAdmin):
    """Admin settings go here."""
    

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

#Company
admin.site.register(Company, ModelAdmin)

#Membership (groups)
admin.site.register(Membership, ModelAdmin)

#Roles
admin.site.register(Role, ModelAdmin)


#Log
admin.site.register(Log, ModelAdmin)

#Objectpermissions
admin.site.register(ObjectPermission, ModelAdmin)

#Profile for users, extending the user
admin.site.register(UserProfile)