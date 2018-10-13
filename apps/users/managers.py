from django.db import models

from apps.common.managers import FetchManager


class UserProfileManager(FetchManager):
    select_related = ("user",)
    prefetch_related = ("addresses",)
