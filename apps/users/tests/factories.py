import factory
import factory.fuzzy
import pytz

from django.contrib.auth.hashers import make_password

from rest_framework.authtoken.models import Token

from ..models import User, UserProfile
from datetime import datetime, timedelta


now = datetime.now(pytz.utc)
three_years_ago = now - timedelta(weeks=52 * 3)
one_years_ago = now - timedelta(weeks=52 * 1)


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Faker("email")
    password = make_password("password", hasher="dummy_hasher")
    date_joined = factory.fuzzy.FuzzyDateTime(three_years_ago, one_years_ago)
    last_login = factory.lazy_attribute(lambda o: o.date_joined + timedelta(days=4))

    class Meta:
        model = User

    @staticmethod
    def create_with_token(**kwargs):
        user = UserFactory(**kwargs)
        Token.objects.create(user=user)
        return user


class UserProfileFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    username = factory.Faker("first_name")

    class Meta:
        model = UserProfile

    @staticmethod
    def create_with_token(**kwargs):
        profile = UserProfileFactory(**kwargs)
        Token.objects.create(user=profile.user)
        return profile
