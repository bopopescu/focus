from django.contrib import admin
from reversion.admin import VersionAdmin
from models import Announcement

class ModelAdmin(VersionAdmin):
    """Admin settings go here."""


admin.site.register(Announcement, ModelAdmin)