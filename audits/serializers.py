from rest_framework import serializers
from .models import ITAuditRequest


class ITAuditRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ITAuditRequest
        fields = [
            "id", "company_name", "contact_person", "email", "phone",
            "employee_count", "infrastructure", "problems", "problems_other",
            "preferred_contact_method", "status", "created_at",
            "traffic_source", "utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term",
        ]
        read_only_fields = ["id", "status", "created_at"]


class ITAuditRequestAdminSerializer(ITAuditRequestSerializer):
    class Meta(ITAuditRequestSerializer.Meta):
        fields = ITAuditRequestSerializer.Meta.fields + ["internal_notes", "lead", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
