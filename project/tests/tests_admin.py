import pytest

from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token


@pytest.fixture
def registered_models():
    return set(admin.site._registry.keys())


@pytest.fixture
def admin_models():
    return {User, Group, Token}


def tests_models_are_correctly_registered(admin_models, registered_models):
    assert registered_models == admin_models


def test_models_are_registered(admin_client, admin_models):
    resp = admin_client.get(reverse("admin:index"), follow=True)
    content = resp.content.decode("utf-8").lower()
    for model in admin_models:
        assert str(model._meta.verbose_name_plural).lower() in content


def test_can_access_add_pages(admin_client, admin_models):
    for model in admin_models:
        app_label = model._meta.app_label
        name = model.__name__.lower()
        url = reverse(f"admin:{app_label}_{name}_add")
        resp = admin_client.get(url)
        assert resp.status_code == status.HTTP_200_OK


def test_can_access_list_pages(admin_client, admin_models):
    for model in admin_models:
        app_label = model._meta.app_label
        name = model.__name__.lower()
        url = reverse(f"admin:{app_label}_{name}_changelist")
        resp = admin_client.get(url)
        assert resp.status_code == status.HTTP_200_OK
