from rest_framework import serializers
from .models import BlogPost, BlogCategory


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ["id", "name", "slug"]


class BlogPostListSerializer(serializers.ModelSerializer):
    category = BlogCategorySerializer(read_only=True)
    author_name = serializers.CharField(source="author.username", read_only=True, default=None)

    class Meta:
        model = BlogPost
        fields = ["id", "title", "slug", "excerpt", "cover_image", "category", "author_name", "created_at"]


class BlogPostDetailSerializer(BlogPostListSerializer):
    class Meta(BlogPostListSerializer.Meta):
        fields = BlogPostListSerializer.Meta.fields + ["content", "seo_title", "seo_description", "updated_at"]
