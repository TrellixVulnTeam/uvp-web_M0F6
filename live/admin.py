from django.contrib import admin

from .models import Feature


class FeatureAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Feature, FeatureAdmin)
