from .factories import ContactFactory


def test_contact_str_method(db):
    contact = ContactFactory()
    assert contact.sender in str(contact)
    assert contact.message[:20] in str(contact)
