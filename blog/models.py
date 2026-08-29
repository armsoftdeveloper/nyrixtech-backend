import uuid
from django.db import models


class BlogCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        verbose_name_plural = "Blog categories"

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=270, unique=True)
    excerpt = models.CharField(max_length=400)
    content = models.TextField()
    cover_image = models.ImageField(upload_to="blog/", blank=True, null=True)
    category = models.ForeignKey(BlogCategory, null=True, blank=True, on_delete=models.SET_NULL, related_name="posts")
    author = models.ForeignKey("users.User", null=True, blank=True, on_delete=models.SET_NULL, related_name="blog_posts")
    published = models.BooleanField(default=False)
    seo_title = models.CharField(max_length=200, blank=True)
    seo_description = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["slug"]), models.Index(fields=["published"])]

    def __str__(self):
        return self.title
