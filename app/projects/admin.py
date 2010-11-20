from django.contrib import admin
from reversion.admin import VersionAdmin
from models import Project

class ProjectModelAdmin(VersionAdmin):
    """Admin settings go here."""

admin.site.register(Project, ProjectModelAdmin)