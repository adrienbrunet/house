from django.urls import reverse

from rest_framework import status

from apps.groups.tests.factories import GroupFactory
from .factories import HousingFactory


def test_get_housing_list_unauth(client):
    url = reverse("housing-list")
    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_housing_list_logged(logged_api_client):
    url = reverse("housing-list")
    response = logged_api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_housing_queryset_is_filtered_correctly(logged_api_client):
    url = reverse("housing-list")
    group = GroupFactory()
    house1 = HousingFactory()
    house2 = HousingFactory(group=group)
    profile = logged_api_client.user.profile
    response = logged_api_client.get(url)
    assert response.json()["count"] == 0

    group.members.add(profile)
    response = logged_api_client.get(url)
    assert response.json()["count"] == 1
