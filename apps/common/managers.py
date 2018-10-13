from django.db import models


class FetchManagerMixin(object):
    """
    This class is intended to be used as a Mixin
    for manager to ease the use of select_related
    and prefetch_related
    """

    use_for_related_fields = True
    select_related = []
    prefetch_related = []

    def get_queryset(self):
        # pylint: disable=no-member
        queryset = super().get_queryset()
        if self.select_related:
            queryset = queryset.select_related(*self.select_related)
        if self.prefetch_related:
            queryset = queryset.prefetch_related(*self.prefetch_related)
        return queryset


class FetchManager(FetchManagerMixin, models.Manager):
    pass


class ArchivableQuerySet(models.QuerySet):
    """
    Replace the delete behavior to switch an "is_archived"
    attribute.
    It also add an archivable method to filter objects
    altered with delete()
    """

    def delete(self):
        self.update(is_archived=True)

    def is_archived(self):
        return self.filter(is_archived=True)

    def active(self):
        return self.filter(is_archived=False)


class ArchivableManager(models.Manager):
    def is_archived(self):
        return self.model.objects.filter(is_archived=True)

    def active(self):
        return self.model.objects.filter(is_archived=False)

    def get_queryset(self):
        return ArchivableQuerySet(self.model, using=self._db)
