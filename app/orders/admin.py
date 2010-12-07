from django.contrib import admin
from core.models import *
from models import *

admin.site.register(Order)
admin.site.register(Task)
admin.site.register(ProjectFile)
admin.site.register(ProjectFolder)