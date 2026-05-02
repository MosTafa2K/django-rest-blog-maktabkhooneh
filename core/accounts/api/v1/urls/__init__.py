from django.urls import path, include


urlpatterns = [
    path("accounts/", include("accounts.api.v1.urls.account")),
    path("profile/", include("accounts.api.v1.urls.profile")),
]