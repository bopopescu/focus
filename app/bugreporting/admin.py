from django.contrib import admin
from models import *
from reversion.admin import VersionAdmin

class ModelAdmin(VersionAdmin):
    """Admin settings go here."""

admin.site.register(Bug, ModelAdmin)
admin.site.register(BugComment, ModelAdmin)