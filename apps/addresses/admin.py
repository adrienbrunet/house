from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Address


class AddressInline(admin.TabularInline):
    model = Address
    verbose_name = _("address")
    verbose_name_plural = _("addresses")
    extra = 1

    def get_queryset(self, request):
        return super().get_queryset(request).active()


admin.site.register(Address)
