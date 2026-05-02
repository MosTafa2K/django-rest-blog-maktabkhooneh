from rest_framework import serializers
from blog.models import Post, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]
        read_only_fields = ["id"]


class PostSerializer(serializers.ModelSerializer):
    snippet = serializers.ReadOnlyField(source="get_snippet")
    relative_url = serializers.URLField(source="get_absolute_api_url", read_only=True)
    absolute_url = serializers.SerializerMethodField()

    def get_absolute_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)

    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        rep["state"] = "list"
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("snippet", None)
            rep.pop("relative_url", None)
            rep.pop("absolute_url", None)
        else:
            rep.pop("body", None)
        rep["category"] = CategorySerializer(instance.category).data
        return rep

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "body",
            "author",
            "image",
            "category",
            "status",
            "snippet",
            "relative_url",
            "absolute_url",
            "published",
            "created",
            "updated",
        ]
        read_only_fields = ["author"]

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["author"] = request.user.profile
        return super().create(validated_data)
