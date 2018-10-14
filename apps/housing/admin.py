from django.contrib import admin

from .models import Housing


@admin.register(Housing)
class HousingAdmin(admin.ModelAdmin):
    list_display = ("name", "group")
    list_filter = ("group",)
