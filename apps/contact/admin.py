from django.contrib import admin

from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("__str__", "sender", "read", "done")
    list_filter = ("read", "done")
