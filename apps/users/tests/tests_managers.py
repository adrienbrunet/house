from apps.addresses.tests.factories import AddressFactory

from ..models import UserProfile
from .factories import UserProfileFactory


def test_user_profile_manager_queries(db, django_assert_num_queries):
    profile = UserProfileFactory()
    AddressFactory.create_batch(2, owner=profile)
    with django_assert_num_queries(2):
        # The second query is the prefetch_related
        profile = UserProfile.objects.get(pk=profile.pk)
        for address in profile.addresses.all():
            address.city
