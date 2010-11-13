import models
from django.contrib import admin
from core.models import *

class OrderModelAdmin(VersionAdmin):
    """Admin settings go here."""

from reversion.admin import VersionAdmin
admin.site.register(Order, OrderModelAdmin)
admin.site.register(Task, OrderModelAdmin)
admin.site.register(ProjectFile, OrderModelAdmin)
admin.site.register(ProjectFolder, OrderModelAdmin)