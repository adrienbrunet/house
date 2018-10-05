import factory
from ..models import Housing


class HousingFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: "House {n}")

    class Meta:
        model = Housing
