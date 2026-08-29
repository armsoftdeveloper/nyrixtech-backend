from django.contrib import admin
from .models import BlogPost, BlogCategory


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author", "published", "created_at")
    list_filter = ("published", "category")
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(BlogCategory)
