from django.db import models
from django.utils.translation import ugettext_lazy as _


class Group(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    heads = models.ManyToManyField(
        "users.UserProfile",
        verbose_name=_("Heads"),
        related_name="managed_groups",
        blank=True,
    )
    members = models.ManyToManyField(
        "users.UserProfile",
        verbose_name=_("Members"),
        related_name="groups",
        blank=True,
    )

    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")

    def __str__(self):
        return self.name

    def get_heads(self):
        return ", ".join([str(el) for el in self.heads.all()])

    def get_members(self):
        return ", ".join([str(el) for el in self.members.all()])
