from .factories import UserFactory


def test_str_method_on_user(db):
    user = UserFactory()
    assert str(user) == user.username
