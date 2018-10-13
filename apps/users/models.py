from django.db import models
from django.utils.translation import gettext_lazy as _

from authtools.models import AbstractEmailUser, UserManager

from .managers import UserProfileManager


class User(AbstractEmailUser):
    """This is the main User model used for auth
    It is not expected to hold a lot of data,
    use the user profile for that.
    """

    objects = UserManager()

    class Meta:
        verbose_name = _("User")


class UserProfile(models.Model):
    """
    UserProfile allows you to hold some data
    that's not directly relevant to authentication.
    Examples: addresses, etc...
    """

    user = models.OneToOneField(
        User, verbose_name=_("User"), related_name="profile", on_delete=models.CASCADE
    )
    username = models.CharField(_("username"), max_length=255, blank=True)

    objects = UserProfileManager()

    class Meta:
        verbose_name = _("Profile")
        verbose_name = _("Profiles")

    def __str__(self):
        return f"{self.user} profile ({self.username})"

    @property
    def handle(self):
        return self.username or str(self.user)
