import factory
from ..models import Housing


class HousingFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: "House {n}")
    group = factory.SubFactory("apps.groups.tests.factories.GroupFactory")

    class Meta:
        model = Housing
