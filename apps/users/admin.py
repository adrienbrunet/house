from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from apps.users.models import User, UserProfile
from apps.addresses.admin import AddressInline


class UserAdmin(BaseUserAdmin):
    list_display = ("email", "is_active", "is_superuser")
    fieldsets = (
        (None, {"fields": ("email", "is_active", "is_superuser")}),
        ("Password", {"fields": ("password",)}),
    )
    add_fieldsets = (
        (None, {"fields": ("email", "is_active", "is_superuser")}),
        (_("Password"), {"fields": ("password1", "password2")}),
    )
    search_fields = ()
    list_filter = ()
    ordering = ("email",)
    filter_horizontal = ()
    filter_vertical = ()
    actions = None


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    inlines = (AddressInline,)


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
