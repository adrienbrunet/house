from ..models import User, UserProfile
from .factories import UserProfileFactory


def test_str_method_for_user():
    user = User(email="test@foo.fr")
    assert str(user) == user.email, str(user)


def test_str_method_for_userprofile():
    user = User(email="test@foo.fr")
    userprofile = UserProfile(user=user, username="foo")
    assert "profile" in str(userprofile)
    assert userprofile.username in str(userprofile)
    assert str(userprofile.username) in str(userprofile)


def test_userprofile_handle_without_username(db):
    profile = UserProfileFactory(username="")
    assert profile.handle == str(profile.user)


def test_userprofile_handle_with_username(db):
    profile = UserProfileFactory(username="Drich")
    assert profile.handle == "Drich"
