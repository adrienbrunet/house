import pytest

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.users.tests.factories import UserFactory, UserProfileFactory


def log_client_with(user, client):
    client.force_login(user)
    client.user = user
    return client


@pytest.fixture
def logged_admin_client(client, db):
    admin = UserFactory(is_superuser=True, is_staff=True)
    return log_client_with(admin, client)


@pytest.fixture
def logged_client(client, db):
    user = UserFactory()
    return log_client_with(user, client)


@pytest.fixture
def logged_api_client(db):
    profile = UserProfileFactory.create_with_token()
    client = APIClient()
    client.user = profile.user
    client.credentials(
        HTTP_AUTHORIZATION="Token " + Token.objects.get(user=profile.user).key
    )
    return client


@pytest.fixture(scope="session")
def anonymous_api_client():
    return APIClient()
