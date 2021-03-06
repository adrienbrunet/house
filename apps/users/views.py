import logging

from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from rest_framework import generics, permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import APIView, ObtainAuthToken
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from apps.addresses.models import Address
from apps.common.uid import decode_uid

from .models import User
from .serializers import (
    LoginSerializer,
    ResetPasswordSerializer,
    UserChangePasswordSerializer,
    UserCreateSerializer,
    UserDetailSerializer,
    UserEmailSerializer,
)
from .services import (
    send_mail_with_confirm_token,
    send_reset_password_mail,
    set_password_user,
)


audit = logging.getLogger("audit").getChild(__name__)


class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()
        audit.info("%r signed up", user, extra={"user": self.request.user})
        send_mail_with_confirm_token(user)


class ObtainAuthTokenView(ObtainAuthToken):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        audit.info("ObtainAuthToken", user, extra={"user": user})
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


class ResetPasswordView(APIView):
    """An endpoint to reset your password being logged out.
    If no reset token is provided, a mail with a link (with token) is sent.
    If it's provided, it allows you to set a new password.
    """

    queryset = User.objects
    permission_classes = (permissions.AllowAny,)

    def _request_password_reset(self, request):
        audit.info("Request Password Reset", extra={"user": request.user})
        serializer = UserEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        audit.info("Request Password Reset Success", extra={"user": request.user})
        send_reset_password_mail(serializer.validated_data.get("email"))

    def _set_new_password_with_reset_token(self, request):
        audit.info("New Password Reset", extra={"user": request.user})
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        audit.info("New Password Reset Success", extra={"user": request.user})
        set_password_user(
            serializer.validated_data.get("uid"), serializer.data.get("password")
        )

    def patch(self, request):
        if "reset_token" in self.request.data:
            self._set_new_password_with_reset_token(request)
        else:
            self._request_password_reset(request)
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class UserChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password when logged in.
    """

    serializer_class = UserChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        return context

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        set_password_user(request.user, serializer.data.get("new_password"))
        return Response(None, status=status.HTTP_204_NO_CONTENT)
