from django.contrib import admin
from models import *

"""
For auto-version of objects
"""
from reversion.admin import VersionAdmin
class ModelAdmin(VersionAdmin):
    """Admin settings go here."""

admin.site.register(File, ModelAdmin)
admin.site.register(Folder, ModelAdmin)