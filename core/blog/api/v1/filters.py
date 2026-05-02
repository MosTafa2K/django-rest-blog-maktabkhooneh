from django.db import models
from django_filters import FilterSet, CharFilter
from blog.models import Post


class PostFilterSet(FilterSet):
    complex_search = CharFilter(
        method="filter_complex_search", label="Complex Search Filter"
    )

    class Meta:
        model = Post
        fields = {"category": ["exact", "in"], "author": ["exact"]}

    def filter_complex_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(title__icontains=value) | models.Q(body__icontains=value)
        )
