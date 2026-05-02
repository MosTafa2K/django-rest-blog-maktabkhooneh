import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from accounts.models.user import User  # noqa


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def dummy_user():
    user = User.objects.create_user(
        username="test_user",
        email="testuser@email.com",
        password="super_secret_password",
        is_verified=True,
    )
    return user


@pytest.mark.django_db
class TestPostAPI:
    def test_api_get_post_response_status_is_success(self, api_client):
        url_path = reverse("blog:v1:post-list")
        response = api_client.get(url_path)
        assert response.status_code == status.HTTP_200_OK

    def test_api_create_post_status_unauthorized(self, api_client):
        url_path = reverse("blog:v1:post-list")
        data = {
            "title": "New Post",
            "body": "New Post Body",
            "status": True,
            "published": timezone.now(),
        }
        response = api_client.post(url_path, data=data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_api_create_post_status_forbidden(self, api_client):
        url_path = reverse("blog:v1:post-list")
        data = {
            "title": "New Post",
            "body": "New Post Body",
            "status": True,
            "published": timezone.now(),
        }
        api_client.force_authenticate(user={})
        response = api_client.post(url_path, data=data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_api_create_post_status_success(self, api_client, dummy_user):
        url_path = reverse("blog:v1:post-list")
        data = {
            "title": "New Post",
            "body": "New Post Body",
            "status": True,
            "published": timezone.now(),
        }
        api_client.force_login(user=dummy_user)
        response = api_client.post(url_path, data=data)
        response_data = response.json()

        assert response.status_code == status.HTTP_201_CREATED
        assert response_data["title"] == data["title"]

    def test_api_create_post_status_bad_request(self, api_client, dummy_user):
        url_path = reverse("blog:v1:post-list")
        data = {
            "title": "New Post",
            "published": timezone.now(),
        }
        api_client.force_login(user=dummy_user)
        response = api_client.post(url_path, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_api_delete_post_unauthorized(self, api_client):
        url_path = reverse("blog:v1:post-detail", kwargs={"pk": 13})
        response = api_client.delete(url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_api_delete_post_success(self, api_client, dummy_user):
        url_path_create = reverse("blog:v1:post-list")
        data = {
            "title": "New Post",
            "body": "New Post Body",
            "status": True,
            "published": timezone.now(),
        }
        api_client.force_login(user=dummy_user)
        response = api_client.post(url_path_create, data=data)
        assert response.status_code == status.HTTP_201_CREATED

        post_id = response.data.get("id")
        assert post_id is not None, "Post created did not include a id"
        url_path_delete = reverse("blog:v1:post-detail", kwargs={"pk": post_id})
        response = api_client.delete(url_path_delete)
        assert response.status_code == status.HTTP_204_NO_CONTENT
