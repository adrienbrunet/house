from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import DjangoUnicodeDecodeError
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from apps.common.uid import decode_uid
from .models import User, UserProfile
from .services import activate_user, set_password_user


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        # Confirmation is required for all users
        user = User(is_active=False, **validated_data)
        set_password_user(user, password)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("username",)


class UserDetailSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ("id", "email", "profile", "last_login")


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def validate_old_password(self, value):
        if not self.context["user"].check_password(value):
            raise serializers.ValidationError(_("Wrong password."))
        return value


class UserEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            return User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(_("No user with this email."))


class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    reset_token = serializers.CharField()
    password = serializers.CharField()

    def validate_uid(self, value):
        try:
            return User.objects.get(id=decode_uid(value))
        except DjangoUnicodeDecodeError:
            raise serializers.ValidationError(_("URL has been tampered with"))
        except User.DoesNotExist:
            raise serializers.ValidationError(_("User not found"))

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        user = data["uid"]
        valid_token = default_token_generator.check_token(user, data["reset_token"])
        if not valid_token:
            raise serializers.ValidationError(
                detail={"reset_token": _("Invalid reset token")}
            )
        return data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"))
    password = serializers.CharField(
        label=_("Password"), style={"input_type": "password"}, trim_whitespace=False
    )
    confirm_token = serializers.CharField(required=False)

    def validate(self, data):
        """
        First, checks user exists and password is correct.
        Then, checks if "confirm_token" is correct when provided.
        If it is, it activates the user or raises an error otherwise.
        """
        try:
            user = User.objects.get(email=data["username"])
        except User.DoesNotExist:
            raise serializers.ValidationError({"username": [_("Invalid email address")]})

        if not user.check_password(data["password"]):
            msg = _("Password is incorrect.")
            raise serializers.ValidationError({"password": [msg]}, code="authorization")

        confirm_token = data.get("confirm_token", None)
        if confirm_token:
            if not default_token_generator.check_token(user, confirm_token):
                raise serializers.ValidationError(
                    _("Invalid confirm token."), code="authorization"
                )
            user = activate_user(user)
        elif not user.is_active:
            raise serializers.ValidationError(
                _("User is not yet confirmed."), code="authorization"
            )
        update_last_login(None, user)
        data["user"] = user
        return data
