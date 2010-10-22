from models import Timetracking, TypeOfTimeTracking
from reversion.admin import VersionAdmin
from django.contrib import admin


class TimetrackingModelAdmin(VersionAdmin):
    """Admin settings go here."""

class TypeOfTimeTrackingModelAdmin(VersionAdmin):
    """Admin settings go here."""

admin.site.register(TypeOfTimeTracking, TypeOfTimeTrackingModelAdmin)
admin.site.register(Timetracking, TimetrackingModelAdmin)