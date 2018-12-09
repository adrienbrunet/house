import pytest

from django.contrib.auth.tokens import default_token_generator
from rest_framework.exceptions import ValidationError

from apps.common.uid import encode_uid

from ..models import User
from ..serializers import (
    LoginSerializer,
    ResetPasswordSerializer,
    UserChangePasswordSerializer,
    UserCreateSerializer,
    UserEmailSerializer,
)
from .factories import UserFactory


def test_password_serializer_with_correct_data(db):
    data = {"old_password": "password", "new_password": "NEW_PASSWORD_UNBREAKABLE"}
    context = {"user": UserFactory()}
    serializer = UserChangePasswordSerializer(data=data, context=context)
    assert serializer.is_valid(), serializer.errors


def test_password_serializer_with_incorrect_data(db):
    data = {"old_password": "OldPassword666", "new_password": "short"}
    context = {"user": UserFactory()}
    serializer = UserChangePasswordSerializer(data=data, context=context)
    assert not serializer.is_valid()


def test_validate_login_serializer_with_confirm_token(db):
    user = UserFactory(is_active=False)
    assert not user.is_active
    token = default_token_generator.make_token(user)
    data = {"username": user.email, "confirm_token": token, "password": "password"}
    serializer = LoginSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    user_updated = User.objects.get(pk=user.pk)
    assert user_updated.is_active


def test_validate_login_with_wrong_email(db):
    data = {"username": "not@¶egistered.com", "password": "password"}
    serializer = LoginSerializer(data=data)
    assert not serializer.is_valid()
    assert "username" in serializer.errors


def test_validate_login_with_wrong_password(db):
    user = UserFactory()
    data = {"username": user.email, "password": "wrong password"}
    serializer = LoginSerializer(data=data)
    assert not serializer.is_valid()
    assert "password" in serializer.errors


def test_validate_login_with_inactive_user(db):
    user = UserFactory(is_active=False)
    data = {"username": user.email, "password": "password"}
    serializer = LoginSerializer(data=data)
    assert not serializer.is_valid()


def test_validate_login_serializer_raise_parse_error_with_wrong_token(db):
    user = UserFactory(is_active=False)
    token = "wrong token"
    data = {"username": user.email, "confirm_token": token, "password": "password"}
    serializer = LoginSerializer(data=data)
    assert not serializer.is_valid()
    with pytest.raises(ValidationError):
        serializer.validate(data=data)


def test_user_change_password_serializer_with_wrong_old_password(db):
    data = {"old_password": "wrong old pwd", "new_password": "foobarbaz"}
    user = UserFactory()
    context = {"user": user}
    serializer = UserChangePasswordSerializer(data=data, context=context)
    serializer.is_valid()
    assert "old_password" in serializer.errors


def test_reset_password_serializer_wrong_uid(db):
    data = {"password": "P@ssword1234", "uid": "WRONG UID"}
    serializer = ResetPasswordSerializer(data=data)
    serializer.is_valid()
    assert "uid" in serializer.errors


def test_reset_password_serializer_uid_with_no_associated_user(db):
    # encode_uid(-1) gives LTE
    data = {"password": "P@ssword1234", "uid": "LTE"}
    serializer = ResetPasswordSerializer(data=data)
    serializer.is_valid()
    assert "uid" in serializer.errors


def test_reset_password_serializer_uid_wrong_reset_token(db):
    user = UserFactory()
    data = {
        "password": "P@ssword1234",
        "uid": encode_uid(user.pk),
        "reset_token": "Wrong token",
    }
    serializer = ResetPasswordSerializer(data=data)
    serializer.is_valid()
    assert "reset_token" in serializer.errors


def test_email_serializer_with_unknow_mail(db):
    serializer = UserEmailSerializer(data={"email": "foo@bar.baz"})
    assert not serializer.is_valid()
