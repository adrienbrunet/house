import factory

from ..models import Address


class AddressFactory(factory.django.DjangoModelFactory):
    street_1 = factory.Sequence(lambda n: f"{n:05d} random street")
    zip_code = factory.Sequence(lambda n: f"{n:07d}")
    city = factory.Sequence(lambda n: f"City {n:05d}")
    country = factory.Sequence(lambda n: f"Country {n:05d}")
    owner = factory.SubFactory("apps.users.tests.factories.UserProfileFactory")

    class Meta:
        model = Address
