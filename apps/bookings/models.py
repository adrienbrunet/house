from django.db import models
from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _


class Booking(models.Model):
    start_date = models.DateTimeField(_("Start date"))
    end_date = models.DateTimeField(_("End date"))
    comments = models.TextField(_("Comments"))
    booker = models.ForeignKey(
        "users.UserProfile", verbose_name=_("Booker"), on_delete=models.CASCADE
    )
    housing = models.ForeignKey(
        "housing.Housing", verbose_name=_("Housing"), on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _("Booking")
        verbose_name_plural = _("Bookings")

    def __str__(self):
        short_comments = Truncator(self.comments).chars(50, truncate="...")
        return f"{self.start_date} - {self.end_date}: {short_comments}"
