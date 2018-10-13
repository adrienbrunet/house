import pytest

from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from apps.users.models import UserProfile
from .factories import AddressFactory


@pytest.fixture
def address_client(db, logged_api_client):
    address = AddressFactory(owner=logged_api_client.user.profile)
    return {
        "client": logged_api_client,
        "address": address,
        "url": reverse("address-list"),
        "detail_url": reverse("address-detail", kwargs={"pk": address.pk}),
        "data": {
            "street1": "1, Cool Street",
            "zip_code": "75011",
            "city": "Paris",
            "country": "France",
        },
    }


def test_list_unauth(anonymous_api_client, address_client):
    response = anonymous_api_client.get(address_client["url"])
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_unauth(anonymous_api_client, address_client):
    response = anonymous_api_client.post(address_client["url"], address_client["data"])
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_unauth(anonymous_api_client, address_client):
    response = anonymous_api_client.delete(
        address_client["detail_url"], address_client["data"]
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_unauth(anonymous_api_client, address_client):
    response = anonymous_api_client.put(
        address_client["detail_url"], address_client["data"]
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_list_when_auth(address_client):
    response = address_client["client"].get(address_client["url"])
    assert response.status_code == status.HTTP_200_OK


def test_create_when_auth(address_client):
    response = address_client["client"].post(
        address_client["url"], address_client["data"], format="json"
    )
    assert response.status_code == status.HTTP_201_CREATED
    # We force reload profile object to bypass prefetch related
    profile = UserProfile.objects.get(pk=address_client["client"].user.profile.pk)
    # Total: 1 from fixtures + 1 newly created
    assert profile.addresses.all().count() == 2


def test_update_when_auth(address_client):
    response = address_client["client"].patch(
        address_client["detail_url"], address_client["data"], format="json"
    )
    assert response.status_code == status.HTTP_200_OK


def test_set_as_primary(address_client):
    response = address_client["client"].patch(
        address_client["detail_url"] + "set_as_primary/"
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["primary"]


def test_delete_when_auth(address_client):
    assert address_client["client"].user.profile.addresses.active().count() == 1
    response = address_client["client"].delete(address_client["detail_url"])
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert address_client["client"].user.profile.addresses.active().count() == 0


def test_user_cant_access_other_users_address(address_client):
    address = AddressFactory()
    url = reverse("address-detail", kwargs={"pk": address.pk})
    response = address_client["client"].get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
