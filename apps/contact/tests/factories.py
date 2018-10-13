import factory
import factory.fuzzy

from ..models import Contact


class ContactFactory(factory.django.DjangoModelFactory):
    sender = factory.LazyAttribute(lambda n: f"contact_mail{n}@example.com")
    message = factory.fuzzy.FuzzyText()

    class Meta:
        model = Contact
