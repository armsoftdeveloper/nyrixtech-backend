from rest_framework import serializers
from .models import Lead, ContactRequest

UTM_FIELDS = ["traffic_source", "utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"]


class ContactRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactRequest
        fields = ["id", "name", "company", "email", "phone", "service", "message", "created_at"] + UTM_FIELDS
        read_only_fields = ["id", "created_at"]


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = [
            "id", "name", "company", "email", "phone", "source",
            "service_interest", "status", "notes", "assigned_to", "created_at", "updated_at",
        ] + UTM_FIELDS
        read_only_fields = ["id", "created_at", "updated_at"]
