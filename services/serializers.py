from rest_framework import serializers
from .models import Service, ServicePlan, Testimonial, FAQ, CaseStudy


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            "id", "name", "slug", "icon", "short_description", "description",
            "features", "order", "seo_title", "seo_description",
        ]


class ServicePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePlan
        fields = [
            "id", "name", "slug", "tagline", "monthly_price", "currency",
            "is_custom_pricing", "features", "is_featured", "order",
        ]


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ["id", "author_name", "author_title", "company", "quote", "is_demo"]


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ["id", "question", "answer", "category", "order"]


class CaseStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseStudy
        fields = ["id", "title", "slug", "industry", "summary", "content", "is_demo", "cover_image", "created_at"]
