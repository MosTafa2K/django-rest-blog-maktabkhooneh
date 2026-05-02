from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .. import views


urlpatterns = [
    path("register/", views.RegisterAPIView.as_view(), name="register-api-view"),
    path(
        "token/create/", views.CustomObtainAuthToken.as_view(), name="auth-token-create"
    ),
    path(
        "token/destroy/",
        views.CustomDestroyAuthToken.as_view(),
        name="auth-token-destroy",
    ),
    path("jwt/create/", TokenObtainPairView.as_view(), name="jwt-create-view"),
    path(
        "jwt/custom/create/",
        views.CustomTokenObtainPairView.as_view(),
        name="jwt-custom-create-view",
    ),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh-view"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify-view"),
    path(
        "password/change/",
        views.ChangePasswordAPIView.as_view(),
        name="change-password-view",
    ),
    # path("activation/confirm/"),
    # path("activation/resend/"),
    path("test-email/", views.TestSendEmail.as_view(), name="send-mail-view"),
]