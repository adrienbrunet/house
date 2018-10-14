from django.urls import path

from . import views


app_name = "users"
urlpatterns = [
    path("me", views.UserDetailView.as_view(), name="me"),
    path(
        "me/password",
        views.UserChangePasswordView.as_view(),
        name="user-change-password",
    ),
    path("auth/signup", views.SignupView.as_view(), name="signup"),
    path("auth/login", views.ObtainAuthTokenView.as_view(), name="login"),
    path("auth/reset", views.ResetPasswordView.as_view(), name="reset-password"),
]
