from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import DjangoUnicodeDecodeError
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from apps.common.uid import decode_uid
from .models import User, UserProfile
from .services import activate_user, set_password_user


def get_user_from_email(email):
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        raise serializers.ValidationError(_("Invalid email address"))


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
        fields = ("id", "email", "profile")


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
        return get_user_from_email(value)


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
    username = serializers.CharField()
    password = serializers.CharField()
    confirm_token = serializers.CharField(required=False)

    def validate_username(self, value):
        return get_user_from_email(value)

    def validate(self, data):
        """
        Checks if "confirm_token" is correct.
        If it is, it activates the user or raise an error otherwise.
        """
        user = self.validate_username(data["username"])
        if not "confirm_token" in data:
            return data

        if not default_token_generator.check_token(user, data["confirm_token"]):
            raise serializers.ValidationError(_("Invalid confirm token"))

        activate_user(user)
        return data
