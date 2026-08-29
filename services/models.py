import uuid
from django.db import models


class Service(models.Model):
    """Top-level IT service offering, e.g. Managed IT, Cybersecurity."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    icon = models.CharField(max_length=64, blank=True, help_text="lucide-react icon name")
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    features = models.JSONField(default=list, blank=True, help_text="List of feature strings")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    seo_title = models.CharField(max_length=200, blank=True)
    seo_description = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "name"]
        indexes = [models.Index(fields=["slug"])]

    def __str__(self):
        return self.name


class ServicePlan(models.Model):
    """Pricing plan tier: STARTER / BUSINESS / ENTERPRISE."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)
    tagline = models.CharField(max_length=200, blank=True)
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=8, default="AMD")
    is_custom_pricing = models.BooleanField(default=False)
    features = models.JSONField(default=list, blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author_name = models.CharField(max_length=150)
    author_title = models.CharField(max_length=150, blank=True)
    company = models.CharField(max_length=150, blank=True)
    quote = models.TextField()
    is_demo = models.BooleanField(default=True, help_text="Mark true unless real client-approved testimonial")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author_name} — {self.company}"


class FAQ(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.CharField(max_length=300)
    answer = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class CaseStudy(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    industry = models.CharField(max_length=120, blank=True)
    summary = models.CharField(max_length=300)
    content = models.TextField()
    is_demo = models.BooleanField(default=True, help_text="Mark true if this is an illustrative example, not a real client")
    cover_image = models.ImageField(upload_to="case_studies/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
