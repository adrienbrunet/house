from datetime import datetime, timedelta
import pytz

import factory
import factory.fuzzy

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.template.defaultfilters import slugify


user_model = get_user_model()
now = datetime.now(pytz.utc)
three_years_ago = now - timedelta(weeks=52 * 3)
one_years_ago = now - timedelta(weeks=52 * 1)


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.lazy_attribute(
        lambda o: slugify(f"{o.first_name}.{o.last_name}")
    )
    email = factory.lazy_attribute(lambda o: f"{o.username}@example.com")
    password = make_password("password", hasher="dummy_hasher")
    date_joined = factory.fuzzy.FuzzyDateTime(three_years_ago, one_years_ago)
    last_login = factory.lazy_attribute(lambda o: o.date_joined + timedelta(days=4))

    class Meta:
        model = user_model
        django_get_or_create = ("username",)
