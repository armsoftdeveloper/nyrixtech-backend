from rest_framework import viewsets, permissions
from .models import BlogPost, BlogCategory
from .serializers import BlogPostListSerializer, BlogPostDetailSerializer, BlogCategorySerializer


class ReadOnlyOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_admin_role)


class BlogCategoryViewSet(viewsets.ModelViewSet):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes = [ReadOnlyOrAdmin]


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.filter(published=True)
    lookup_field = "slug"
    permission_classes = [ReadOnlyOrAdmin]
    filterset_fields = ["category"]
    search_fields = ["title", "excerpt"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BlogPostDetailSerializer
        return BlogPostListSerializer
