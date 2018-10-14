import pytest

from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.common.uid import encode_uid

from ..models import User
from .factories import UserFactory


anonymous_client = APIClient()


@pytest.fixture
def user(db):
    return UserFactory.build()


@pytest.fixture
def user_with_token(db):
    return UserFactory.create_with_token()


def test_user_detail_view_unauthed(anonymous_api_client):
    url = reverse("users:me")
    response = anonymous_api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_user_detail_view_authed(logged_api_client):
    url = reverse("users:me")
    response = logged_api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_register_valid_user(db, user):
    signup_url = reverse("users:signup")
    data = {"email": user.email, "password": user.password}
    response = anonymous_client.post(signup_url, data, format="json")

    assert response.status_code, status.HTTP_201_CREATED
    assert User.objects.count() == 1
    assert User.objects.get().email == user.email


def test_register_invalid_user():
    signup_url = reverse("users:signup")
    required_fields = ("email", "password")
    data = {"username": "foo"}
    response = anonymous_client.post(signup_url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    for k in required_fields:
        assert k in response.data


def test_login_user_wrong_password(logged_client):
    url = reverse("users:login")
    data = {"username": logged_client.user.email, "password": "wrong_password"}
    response = logged_client.post(url, data=data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_valid_login(user_with_token):
    login_url = reverse("users:login")
    data = {"username": user_with_token.email, "password": "password"}
    response = anonymous_client.post(login_url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.data


def test_invalid_login(user):
    login_url = reverse("users:login")
    data = {"username": user.email, "password": "wrong_password"}
    response = anonymous_client.post(login_url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_login_user_inactive(logged_client):
    url = reverse("users:login")
    logged_client.user.is_active = False
    logged_client.user.save()
    data = {"username": logged_client.user.email, "password": "password"}
    response = logged_client.post(url, data=data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_reset_password_generate(logged_api_client):
    data = {"email": logged_api_client.user.email}
    response = logged_api_client.patch(
        reverse("users:reset-password"), data, format="json"
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_reset_password_confirm(logged_api_client):
    reset_token = default_token_generator.make_token(logged_api_client.user)
    password = "ComplicatedPassword1234 battery horse staples"
    data = {
        "password": password,
        "uid": encode_uid(logged_api_client.user.id),
        "reset_token": reset_token,
    }
    response = logged_api_client.patch(
        reverse("users:reset-password"), data, format="json"
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    user = User.objects.get(id=logged_api_client.user.id)
    assert user.check_password(password)


def test_change_password_with_correct_password(logged_api_client):
    url = reverse("users:user-change-password")
    response = logged_api_client.patch(
        url,
        data={"old_password": "password", "new_password": "P@ssw0rd1234"},
        format="json",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
