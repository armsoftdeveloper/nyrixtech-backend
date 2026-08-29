from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "company", "uploaded_by", "title", "category", "file", "created_at"]
        read_only_fields = ["id", "uploaded_by", "created_at"]
