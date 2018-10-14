import factory

from ..models import Group


class GroupFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Group n°{n}")

    class Meta:
        model = Group
