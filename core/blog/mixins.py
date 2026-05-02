from django.http import Http404
from django.shortcuts import get_object_or_404
from .models import Post


class AuthorAccessMixin:
    def dispatch(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        if post.author == request.user or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("You haven't enough permissions to access this page!")
