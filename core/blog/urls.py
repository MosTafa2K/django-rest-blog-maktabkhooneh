from django.urls import include, path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index-view"),
    path("posts/", views.PostListView.as_view(), name="posts-list-view"),
    path("posts/api/", views.PostListAPIView.as_view(), name="posts-list-api-view"),
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name="post-detail-view"),
    path("posts/create/", views.PostCreateView.as_view(), name="post-create-view"),
    path("posts/<int:pk>/edit/", views.PostEditView.as_view(), name="post-edit-view"),
    path(
        "posts/<int:pk>/delete/",
        views.PostDeleteView.as_view(),
        name="post-delete-view",
    ),
    # path("api/v1/", include("blog.api.v1.urls", namespace="blog_api_v1")),
    path(
        "api/v1/", include(("blog.api.v1.urls", "blog_api_v1"), namespace="blog_api_v1")
    ),
]
