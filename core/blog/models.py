from django.db import models
from django.contrib.auth import get_user_model  # noqa


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField()
    author = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)
    status = models.BooleanField()
    published = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_name(self):
        return self.author.first_name or "No name"

    def get_snippet(self):
        return self.body[:8]

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
