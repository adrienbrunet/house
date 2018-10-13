import factory

from apps.users.tests.factories import UserProfileFactory
from ..models import Address
from .factories import AddressFactory


def test_address_str(db):
    adr = AddressFactory()
    assert "street" in str(adr)
    assert ", City " in str(adr)


def test_save_user_ensure_only_one_address_is_set_as_primary(db):
    profile = UserProfileFactory()
    address1 = AddressFactory(owner=profile)
    address2 = AddressFactory(owner=profile)
    address3 = AddressFactory(owner=profile)
    address1.primary = True
    address2.primary = True
    address3.primary = True
    address1.save()
    address2.save()
    address3.save()

    addresses = profile.addresses.all()
    assert len([add for add in addresses if add.primary]) == 1


def test_set_as_primary(db):
    address = AddressFactory()
    address.set_as_primary()
    assert address.primary


def test_deletion_only_toggle_is_archived_for_model(db):
    address = AddressFactory()
    address.delete()
    non_deleted = Address.objects.get(pk=address.pk)
    assert non_deleted.is_archived


def test_deletion_only_toggle_is_archived_for_addresses_queryset(db):
    AddressFactory.create_batch(2)
    addresses = Address.objects.all()
    addresses.delete()
    deleted_addresses = Address.objects.all()
    assert len(deleted_addresses) == 2
    assert all([el.is_archived for el in addresses])


def test_is_archived_manager_method_on_addresses(db):
    add1, add2 = AddressFactory.create_batch(2)
    add1.delete()
    archived_addresses = Address.objects.is_archived()
    assert len(archived_addresses) == 1
    assert archived_addresses[0].is_archived


def test_is_archived_queryset_method_on_addresses(db):
    add1, add2 = AddressFactory.create_batch(2)
    add1.delete()
    archived_addresses = Address.objects.all().is_archived()
    assert len(archived_addresses) == 1
    assert archived_addresses[0].is_archived
