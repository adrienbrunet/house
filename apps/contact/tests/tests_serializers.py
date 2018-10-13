from ..serializers import ContactSerializer


def test_contact_serializer_with_valid_data():
    data = {
        "sender": "foo@bar.com",
        "message": "I'm so happy with everything this app provides, you're amazing. Lov, <3 <3",
    }
    assert ContactSerializer(data=data).is_valid()


def test_contact_serializer_with_wrong_mail():
    data = {
        "sender": "NOT A MAIL",
        "message": "I'm so happy with everything this app provides, you're amazing. Lov, <3 <3",
    }
    serializer = ContactSerializer(data=data)
    assert not serializer.is_valid()
    assert "sender" in serializer.errors


def test_contact_serializer_with_no_sender():
    data = {"message": "BliBlaBlo"}
    serializer = ContactSerializer(data=data)
    assert not serializer.is_valid()
    assert "sender" in serializer.errors


def test_contact_serializer_with_no_message():
    data = {"sender": "sender@mail.com"}
    serializer = ContactSerializer(data=data)
    assert not serializer.is_valid()
    assert "message" in serializer.errors
