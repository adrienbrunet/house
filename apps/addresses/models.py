from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.common.managers import ArchivableManager
from apps.common.models import ArchivableModel

from apps.users.models import UserProfile


class Address(ArchivableModel):
    """
    Generic model to store addresses for UserProfiles.
    It can be used for housing, billing, etc...
    """

    street_1 = models.CharField(_("Address line 1"), max_length=255)
    street_2 = models.CharField(_("Address line 2"), max_length=255, blank=True)
    zip_code = models.CharField(_("Zip code"), max_length=255)
    city = models.CharField(_("City"), max_length=255)
    country = models.CharField(_("Country"), max_length=255)
    primary = models.BooleanField(_("Primary address"), default=False)
    owner = models.ForeignKey(
        UserProfile,
        verbose_name=_("Owner"),
        on_delete=models.CASCADE,
        related_name="addresses",
    )

    objects = ArchivableManager()

    class Meta:
        verbose_name = _("address")
        verbose_name_plural = _("addresses")

    def __str__(self):
        return ", ".join(self.get_relevant_fields())

    def get_relevant_fields(self):
        """
        Return a tuple with the relevant fields
        to display the full address
        """
        relevant_fields = (
            self.street_1,
            self.street_2,
            self.zip_code,
            self.city,
            self.country,
        )
        return (el for el in relevant_fields if el)

    def set_as_primary(self):
        self.primary = True
        self.save()

    def save(self, *args, **kwargs):
        """
        Only one address can be the primary address for a given profile
        """
        super().save(*args, **kwargs)
        self.ensure_unicity_for_primary_address()

    def ensure_unicity_for_primary_address(self):
        """
        If this address is the primary one,
        set all others as non primary
        """
        if self.primary:
            self.owner.addresses.exclude(pk=self.id).update(primary=False)
