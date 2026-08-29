from rest_framework import viewsets, permissions
from .models import Service, ServicePlan, Testimonial, FAQ, CaseStudy
from .serializers import (
    ServiceSerializer, ServicePlanSerializer, TestimonialSerializer, FAQSerializer, CaseStudySerializer
)


class ReadOnlyOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_admin_role)


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    lookup_field = "slug"
    permission_classes = [ReadOnlyOrAdmin]


class ServicePlanViewSet(viewsets.ModelViewSet):
    queryset = ServicePlan.objects.filter(is_active=True)
    serializer_class = ServicePlanSerializer
    permission_classes = [ReadOnlyOrAdmin]


class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.filter(is_active=True)
    serializer_class = TestimonialSerializer
    permission_classes = [ReadOnlyOrAdmin]


class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.filter(is_active=True)
    serializer_class = FAQSerializer
    permission_classes = [ReadOnlyOrAdmin]


class CaseStudyViewSet(viewsets.ModelViewSet):
    queryset = CaseStudy.objects.filter(is_active=True)
    serializer_class = CaseStudySerializer
    lookup_field = "slug"
    permission_classes = [ReadOnlyOrAdmin]
