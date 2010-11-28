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

admin.site.unregister(FlatPage)

#Company
admin.site.register(Company, ModelAdmin)

#Membership (groups)
admin.site.register(Membership, ModelAdmin)

#Roles
admin.site.register(Role, ModelAdmin)


#Log
admin.site.register(Log, ModelAdmin)

#Objectpermissions
admin.site.register(Permission, ModelAdmin)

#Profile for users, extending the user
admin.site.register(UserProfile)