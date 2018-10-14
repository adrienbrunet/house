from django.urls import reverse

from rest_framework import status

from apps.groups.tests.factories import GroupFactory


def test_get_group_list_unauth(client):
    url = reverse("group-list")
    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_group_list_logged(logged_api_client):
    url = reverse("group-list")
    response = logged_api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_group_queryset_is_filtered_correctly(logged_api_client):
    url = reverse("group-list")
    group = GroupFactory()
    profile = logged_api_client.user.profile
    response = logged_api_client.get(url)
    assert response.json()["count"] == 0

    group.members.add(profile)
    response = logged_api_client.get(url)
    assert response.json()["count"] == 1
