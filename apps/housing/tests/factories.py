import factory
from ..models import Housing


class HousingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Housing
