from models import *
from django.contrib import admin
from reversion.admin import VersionAdmin
class ModelAdmin(VersionAdmin):
    """Admin settings go here."""

admin.site.register(UnitsForSizes, ModelAdmin)
admin.site.register(ProductCategory, ModelAdmin)
admin.site.register(ProductGroup, ModelAdmin)
admin.site.register(Currency, ModelAdmin)
admin.site.register(Product, ModelAdmin)
