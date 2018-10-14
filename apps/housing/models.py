from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


user_model = get_user_model()


class Housing(models.Model):
    """
    This is the main model to hold Housing data
    and relations to others models.
    """

    name = models.CharField(_("name"), max_length=255)
    group = models.ForeignKey(
        "groups.Group",
        verbose_name=_("Group"),
        on_delete=models.CASCADE,
        related_name="housing",
    )

    class Meta:
        verbose_name = _("housing")
        verbose_name_plural = _("housing")

    def __str__(self):
        return self.name
