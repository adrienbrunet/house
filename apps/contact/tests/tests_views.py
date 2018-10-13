from django.urls import reverse

from rest_framework import status


def test_contact_with_get_method(client):
    url = reverse("contact")
    response = client.get(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_contact_with_post_method_and_correct_data(anonymous_api_client, db):
    url = reverse("contact")
    data = {"sender": "foo@bar.baz", "message": "Yop, wazza"}
    response = anonymous_api_client.post(url, data=data, format="json")
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.content
