import pytest

from django.contrib import admin
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token

from apps.addresses.models import Address
from apps.contact.models import Contact
from apps.groups.models import Group
from apps.housing.models import Housing
from apps.users.models import User, UserProfile
from apps.bookings.models import Booking


@pytest.fixture
def registered_models():
    return set(admin.site._registry.keys())


@pytest.fixture
def admin_models():
    return {Address, Booking, Contact, Group, Housing, Token, User, UserProfile}


def tests_models_are_correctly_registered(admin_models, registered_models):
    assert registered_models == admin_models


def test_models_are_registered(logged_admin_client, admin_models):
    resp = logged_admin_client.get(reverse("admin:index"), follow=True)
    content = resp.content.decode("utf-8").lower()
    for model in admin_models:
        assert str(model._meta.verbose_name_plural).lower() in content


def test_can_access_add_pages(logged_admin_client, admin_models):
    for model in admin_models:
        app_label = model._meta.app_label
        name = model.__name__.lower()
        url = reverse(f"admin:{app_label}_{name}_add")
        resp = logged_admin_client.get(url)
        assert resp.status_code == status.HTTP_200_OK


def test_can_access_list_pages(logged_admin_client, admin_models):
    for model in admin_models:
        app_label = model._meta.app_label
        name = model.__name__.lower()
        url = reverse(f"admin:{app_label}_{name}_changelist")
        resp = logged_admin_client.get(url)
        assert resp.status_code == status.HTTP_200_OK
