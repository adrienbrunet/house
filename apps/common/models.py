from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import ArchivableManager


class ArchivableModel(models.Model):
    """
    Use 'is_archived' boolean instead of classic delete method
    """

    is_archived = models.BooleanField(_("is_archived"), default=False, editable=False)

    objects = ArchivableManager()

    class Meta:
        abstract = True

    def delete(self):
        self.is_archived = True
        self.save()
