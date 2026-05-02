from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from blog.models import Category, Post

from .permissions import IsOwnerOrReadOnly
from .serializers import CategorySerializer, PostSerializer
from .paginations import CustomPaginator
from .filters import PostFilterSet


class PostListAPIView(generics.ListCreateAPIView):
    """Handles post listing and creation using APIView.

    Supports both `GET` for retrieving posts and `POST` for creating new ones.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.profile)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """Handles get, update and delete opetations for a specific post.

    Supports `GET` for retrieve post, `PUT` for updating post and `DELETE` for deleting post.

    - Note: `PUT` and `DELETE` operations will only available for owner of post.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.order_by("id").all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    # filterset_fields = {"category": ["exact", "in"], "author": ["exact"]}
    filterset_class = PostFilterSet
    search_fields = ["body", "title"]
    pagination_class = CustomPaginator
    pagination_class.page_size = 3

    @action(detail=False, url_name="available-posts", url_path="available-posts")
    def get_all_available_posts(self, request):
        posts = Post.objects.filter(status=True)
        serializer = self.serializer_class(
            posts, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @action(detail=False, url_name="unavailable-posts", url_path="unavailable-posts")
    def get_all_unavailable_posts(self, request):
        posts = Post.objects.filter(status=False)
        serializer = self.serializer_class(
            posts, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @method_decorator(cache_page(60 * 15, key_prefix="posts_list"))
    def list(self, request, *args, **kwargs):
        import time

        time.sleep(5)
        return super().list(request, *args, **kwargs)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.order_by("id").all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
